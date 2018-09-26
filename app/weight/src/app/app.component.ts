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
          if (courrier.courrier) {
            if (courrier.courrier === 'Estafeta_barato') {
              this.pakkePrice = courrier.price;
            } else if (courrier.courrier === 'Estafeta_caro') {
              this.price = courrier.price;
            }
          }
        });
        this.percent = Math.abs(((this.pakkePrice - this.price) * 100) / this.pakkePrice);
      });
    });
  }

}
