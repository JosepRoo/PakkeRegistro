import { Component, OnInit, Input } from '@angular/core';
import { MatIconRegistry } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.css']
})
export class CheckComponent implements OnInit {

  @Input('response') shipment: any;
  @Input('service') service: any;
  @Input('card') card: any;
  @Input('order') order: any;
  private pdfUrl: any;
  private preview: any;

  constructor(
    private iconRegistry   : MatIconRegistry,
    private sanitizer      : DomSanitizer,
  ) {
    this.iconRegistry
    .addSvgIcon('calendar', sanitizer.bypassSecurityTrustResourceUrl('./assets/calendar.svg'))
    .addSvgIcon('mexico', sanitizer.bypassSecurityTrustResourceUrl('./assets/mexico.svg'))
    .addSvgIcon('scale', sanitizer.bypassSecurityTrustResourceUrl('./assets/scale.svg'))
    .addSvgIcon('mastercard', sanitizer.bypassSecurityTrustResourceUrl('./assets/mastercard.svg'))
    .addSvgIcon('visa', sanitizer.bypassSecurityTrustResourceUrl('./assets/visa.svg'))
    .addSvgIcon('amex', sanitizer.bypassSecurityTrustResourceUrl('./assets/amex.svg'))
    .addSvgIcon('box', sanitizer.bypassSecurityTrustResourceUrl('./assets/icn_box.svg'))
    .addSvgIcon('company', sanitizer.bypassSecurityTrustResourceUrl('./assets/icn_building.svg'))
    .addSvgIcon('calendar', sanitizer.bypassSecurityTrustResourceUrl('./assets/calendar.svg'))
    .addSvgIcon('mexico', sanitizer.bypassSecurityTrustResourceUrl('./assets/mexico.svg'))
    .addSvgIcon('clock', sanitizer.bypassSecurityTrustResourceUrl('./assets/clock.svg'))
    .addSvgIcon('dollar', sanitizer.bypassSecurityTrustResourceUrl('./assets/dollar-coins.svg'))
    .addSvgIcon('bank', sanitizer.bypassSecurityTrustResourceUrl('./assets/bank.svg'))
    .addSvgIcon('dollar-pink', sanitizer.bypassSecurityTrustResourceUrl('./assets/money-bag.svg'))
    .addSvgIcon('kilo', sanitizer.bypassSecurityTrustResourceUrl('./assets/kilogram.svg'))
    .addSvgIcon('folder', sanitizer.bypassSecurityTrustResourceUrl('./assets/folder.svg'))
    .addSvgIcon('truck', sanitizer.bypassSecurityTrustResourceUrl('./assets/truck.svg'))
    .addSvgIcon('box', sanitizer.bypassSecurityTrustResourceUrl('./assets/box.svg'))
  }

  ngOnInit() {
    this.createPdf(this.shipment.Label);
  }

  createPdf(b64Data) {
    var contentType = 'pdf';
    var sliceSize = 1024;

    var byteCharacters = atob(b64Data);
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      var slice = byteCharacters.slice(offset, offset + sliceSize);

      var byteNumbers = new Array(slice.length);
      for (var i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }

      var byteArray = new Uint8Array(byteNumbers);

      byteArrays.push(byteArray);
    }

    var blob = new Blob(byteArrays, {type: contentType});
    var blobUrl = URL.createObjectURL(blob);
    this.pdfUrl = blobUrl;
  }

  printPdf(b64Data) {
    var contentType = 'application/pdf';
    var sliceSize = 512;
    var byteCharacters = window.atob(b64Data);
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    var blob = new Blob(byteArrays, {type: contentType});
    var url = URL.createObjectURL(blob);
    var newWindow = window.open(url);
  }

  setEstimatedDate(days){
    var now = new Date();
    now.setDate(now.getDate() + Number(days) );
    return now;
  }

}
