import { WeightService } from './weight.service';
import { Component, OnInit } from '@angular/core';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'Pakke-Scales';
  sub: Subscription;
  source = interval(2000);
  weight: any = 0;
  price: any = 0;
  pakkePrice: any = 0;
  percent: any = 0;

  constructor(
    private weightService: WeightService
  ) {}

  ngOnInit() {
    this.sub = this.source.subscribe(_res => {
      this.weightService.getData().subscribe(res => {
        this.weight = res.weight;
        res.result.forEach(courrier => {
          if (courrier.price) {
            if (courrier.price.ESTAFETA_TERRESTRE_CONSUMO) {
              this.pakkePrice = courrier.price.ESTAFETA_TERRESTRE_CONSUMO.price;
            } else if (courrier.price.AEROFLASH_TERRESTRE) {
              this.price = courrier.price.AEROFLASH_TERRESTRE;
            }
          }
        });
        this.percent = ((this.pakkePrice - this.price) * 100) / this.pakkePrice;
      });
    });
  }

}
