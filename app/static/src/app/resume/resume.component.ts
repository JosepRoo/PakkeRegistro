import { Component, OnInit, Input } from '@angular/core';
import { MatIconRegistry } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-resume',
  templateUrl: './resume.component.html',
  styleUrls: ['./resume.component.css']
})
export class ResumeComponent implements OnInit {

  @Input('service') service: any;
  @Input('origin') origin: any;
  @Input('destiny') destiny: any;
  @Input('product') product: any;

  constructor(
    private iconRegistry   : MatIconRegistry,
    private sanitizer      : DomSanitizer,
  ) {
    this.iconRegistry
    .addSvgIcon('calendar', sanitizer.bypassSecurityTrustResourceUrl('./assets/calendar.svg'))
    .addSvgIcon('mexico', sanitizer.bypassSecurityTrustResourceUrl('./assets/mexico.svg'))
    .addSvgIcon('scale', sanitizer.bypassSecurityTrustResourceUrl('./assets/scale.svg'))
  }

  ngOnInit() {
  }

  setEstimatedDate(days){
    var now = new Date();
    now.setDate(now.getDate() + Number(days) );
    return now;
  }

  getWeight(product) {
    var weight = (product.width * product.height * product.deep)/5000
    if (weight > product.weight){
      return weight;
    }
    return product.weight;
  }

}
