'use strict';

const Crawler = require('crawler');
const fs = require('fs');
const moment = require('moment');
const logger = require('winston');

const _prgname = 'zillow.sold25-26-2';

const left = -122550000;
const right = -122500000;
logger.cli();
logger.add(logger.transports.File, {
  filename: './log/' + _prgname + '.' + moment().format('YYYY-MM-DD') + '.log'
});

function House() {
  let self = this;
  self.today = moment().format('YYYY-MM-DD');
  self.resultDir = './result/';
  self.resultFile = self.resultDir + _prgname + '_' + self.today + '.csv';
  self.crawler = new Crawler({
    maxConnections: 1,
    rateLimit: 3000,
    logger: logger,
    debug: false,
    headers: {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
  });

  self.crawler.on('drain', function() {
    logger.info('job done.');
  });
}

House.prototype.init = function() {
  let self = this;

  if (!fs.existsSync(self.resultDir)) {
    fs.mkdirSync(self.resultDir);
  }
  fs.writeFileSync(self.resultFile, 'Status,zpid,Address,City,Zip,Beds,Baths,Square,Zestimate,Sale,Longitude,Latitude,Days,Views,Saves,LastSoldDate,LastSoldPrice,Feature,Date\n');
};

House.prototype.start = function() {
  let self = this;

  self.init();
  for (let x = left; x < right; x += 1000) {
    let url = `https://www.zillow.com/search/GetResults.htm?spt=homes&status=001000&lt=000000&ht=111111&pr=,&mp=,&bd=2%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&fr-bldg=0&furnished-apartments=0&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&sch=100111&zoom=9&rect=${x},37201894,${x+1000},38530442&sort=globalrelevanceex&search=maplist&listright=true&isMapSearch=1&p=`;
    self.getList(url, 1);
  }
};

House.prototype.getList = function(url, page) {
  let self = this;

  self.crawler.queue({
    uri: url + page,
    callback: function(err, result, done) {
      if (err) {
        logger.error(err);
        return done();
      }


      let json = null;
      try {
       json = JSON.parse(result.body);
      } catch (e){
        console.log(result.body);
        setTimeout(self.getList, 30000, url, page);
        return done();
      }

      let pageNum = Math.min(20, json.list.numPages);
      for (let i = 2; i <= pageNum; i++) {
        self.getList(url, i);
      }

      json.list.zpids.forEach(zpid => {
        self.getDetails(zpid);
      });

      logger.info(`Search [${url.match(/rect=(.*)&sort/)[1]}], page: ${page}/${json.list.numPages}`);
      return done();
    }
  });
};

House.prototype.getDetails = function(zpid) {
  let self = this;

  self.crawler.queue({
    uri: `https://www.zillow.com/homedetails/${zpid}_zpid/`,
    callback: function(err, result, done) {
      if (err) {
        logger.error(err);
        return done();
      }

      let $ = result.$;
      let gene = {};
      let header = $('.zsg-content-header');
      console.log(result.options.uri);
      let features = [];
      gene.zpid = zpid;
      if (header.length !== 0) {
        let nameSplit = header.children('.notranslate').text().split(',');
        gene.address = nameSplit[0];
        gene.city = nameSplit[1];
        gene.zip = nameSplit[2];
        let size = header.find('.addr_bbs');
        gene.beds = size.eq(0).text();
        gene.baths = size.eq(1).text();
        gene.square = size.eq(2).text().replace(/,/g, '');
        let price = $('#home-value-wrapper').find('.main-row').text().replace(/[,$]/g, '').trim().match(/\d+/);
        gene.sale = price == null ? 'N/A' : price[0];
        gene.zestimate = $('#home-value-wrapper').find('.home-summary-row').eq(2).children('span').eq(1).text().replace(/[,$]/g, '').trim();
        let length = $('.zsg-media-bd').length;
        for (let i = 0; i < length; i++) {
          features.push($('.zsg-media-bd').eq(i).children('p').text().replace(/,/g, '').trim() + ':' + $('.zsg-media-bd').eq(i).children('div').text().replace(/,/g, '').trim());
        }
        gene.longitude = $('[itemprop="longitude"]').attr('content');
        gene.latitude = $('[itemprop="latitude"]').attr('content');
        let containerLen = $('.hdp-fact-list > li').length;
        gene.days = 'N/A';
        gene.views = 'N/A';
        gene.saves = 'N/A';
        gene.lastSoldDate = 'N/A';
        gene.lastSoldPrice = 'N/A';

        for (let i = 0; i < containerLen; i++) {
          let label = $('.hdp-fact-list > li').eq(i).find('.hdp-fact-name').text();
          //        console.log(label);
          //        console.log(label.match(/Days\s*on\s*Zillow/) !== null);
          if (label.match(/Days\s*on\s*Zillow/) !== null) {
            gene.days = $('.hdp-fact-list > li').eq(i).find('.hdp-fact-value').text().replace(/,/, '');
          }
          else if (label.match(/Views\s*since\s*listing/i) !== null) {
            gene.views = $('.hdp-fact-list > li').eq(i).find('.hdp-fact-value').text().replace(/,/, '');
          }
          else if (label.match(/Last\s*sold/) !== null) {
            let sold = $('.hdp-fact-list > li').eq(i).find('.hdp-fact-value').text().split('for');
            gene.lastSoldDate = sold[0];
            gene.lastSoldPrice = sold[1].replace(/[$,]/g, '').trim();
          }
          let saves = $('.hdp-fact-list > li').eq(i).find('.hdp-fact-value').text().match(/(\d*)\sshoppers\ssaved/);
          if (saves !== null) {
            gene.saves = saves[1].replace(/,/, '');
          }
        }

      }
      else {
        header = $('.zsg-content-item');
        let nameSplit = header.children('.zsg-h1').children('.zsg-h2').text().split(',');
        gene.address = header.children('.zsg-h1').children('.zsg-h1').text();
        gene.city = nameSplit[0];
        gene.zip = nameSplit[1];
        let size = header.children('h3').children('span');
        gene.beds = size.eq(1).text();
        gene.baths = size.eq(3).text();
        gene.square = size.eq(5).text().replace(/,/g, '');
        let match = result.body.match(/zestimate":\s*(\d*)/);
        gene.zestimate = match === null ? "N/A" : match[1];
        gene.sale = $('.price').text().replace(/[,$]/g, '').trim();
        let length = $('.zsg-media-bd').length;
        for (let i = 0; i < length; i++) {
          features.push($('.zsg-media-bd').eq(i).children('.fact-label').text().replace(/,/g, '').trim() + ':' + $('.zsg-media-bd').eq(i).children('.fact-value').text().replace(/,/g, '').trim());
        }
        let longitude = result.body.match(/longitude":\s*(-*\d*\.\d*),/);
        let latitude = result.body.match(/latitude":\s*\\*(-*\d*\.\d*),/);
        gene.longitude = longitude === null ? 0 : longitude[1];
        gene.latitude = latitude === null ? 0 : latitude[1];
        let containerLen = $('.fact-container').length;
        gene.days = 'N/A';
        gene.views = 'N/A';
        gene.saves = 'N/A';
        gene.lastSoldDate = 'N/A';
        gene.lastSoldPrice = 'N/A';

        for (let i = 0; i < containerLen; i++) {
          let label = $('.fact-container').eq(i).find('.fact-label').text();
          //        console.log(label);
          //        console.log(label.match(/Days\s*on\s*Zillow/) !== null);
          if (label.match(/Days\s*on\s*Zillow/) !== null) {
            gene.days = $('.fact-container').eq(i).find('.fact-value').text().replace(/,/, '');
          }
          else if (label.match(/Views\s*since\s*listing/i) !== null) {
            gene.views = $('.fact-container').eq(i).find('.fact-value').text().replace(/,/, '');
          }
          else if (label.match(/Last\s*sold/) !== null) {
            let sold = $('.fact-container').eq(i).find('.fact-value').text().split('for');
            gene.lastSoldDate = sold[0];
            gene.lastSoldPrice = sold[1].replace(/[$,]/g, '').trim();
          }
          let saves = $('.fact-container').eq(i).find('.fact-value').text().match(/(\d*)\sshoppers\ssaved/);
          if (saves !== null) {
            gene.saves = saves[1].replace(/,/, '');
          }
        }
      }

      gene.features = features.join(';');
//    gene.providedBy = $('#listing-provided-by').
      //     console.log(gene);
      let row = [
        "status",
        gene.zpid,
        gene.address,
        gene.city,
        gene.zip,
        gene.beds,
        gene.baths,
        gene.square,
        gene.zestimate,
        gene.sale,
        gene.longitude,
        gene.latitude,
        gene.days,
        gene.views,
        gene.saves,
        gene.lastSoldDate,
        gene.lastSoldPrice,
        gene.features,
        self.today
      ].map(item => {
        item += '';
        return item.trim().replace(/[\s,"]+/g, ' ');
      }).join();
      fs.appendFileSync(self.resultFile, row + '\n');
//    console.log(gene);
      logger.info(`Get ${zpid} details`);
      return done();
    }
  });
};

const that = new House();
that.start();

