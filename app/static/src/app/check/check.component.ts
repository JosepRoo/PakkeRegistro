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
  }

  ngOnInit() {
  }

}
