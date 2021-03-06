import { WeightService } from './weight.service';
import { Component, OnInit } from '@angular/core';
import { interval, Subscription } from 'rxjs';
import { HostListener } from '@angular/core';

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

  @HostListener('window:keydown', ['$event'])
  handleKeyDown(event: KeyboardEvent) {
    if (event.code === 'Space') {
      this.print();
    }
  }

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
        let percent = ((this.price - this.pakkePrice) * 100) / this.price;
        if (percent < 0) {
          percent = percent * (-1);
        }
        this.percent = percent;
      });
    });
  }

  print() {
    const data = {
     public_price: this.price,
     pakke_price: this.pakkePrice,
     weight: this.weight
    };
    this.weightService.print(data).subscribe(res => {
      console.log(res);
    });
  }

}
