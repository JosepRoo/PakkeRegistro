import { QuoteService } from './quote.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  guide: FormGroup;
  services = [];
  prices = [];
  response: any;

  constructor(private formBuilder: FormBuilder, private quoteService: QuoteService) {}

  ngOnInit() {
    this.guide = this.formBuilder.group({
      pakke_key: ['3Gb4HTCSRHFzqdgyY9HKmSCUhC5E'],
      courrier_services: this.formBuilder.group({
        name: ['', Validators.required],
        type: ['', Validators.required]
      }),
      weight: ['21', Validators.required],
      width: [1],
      height: [1],
      length: [1],
      origin_zipcode: ['38078', Validators.required],
      destiny_zipcode: ['96520', Validators.required]
    });
  }

  courrierChanged() {
    // console.log(this.guide.controls.courrier_services);
    const group = this.guide.controls.courrier_services as FormGroup;
    const courrier = group.controls.name.value;
    switch (courrier) {
      case 'DHL':
        this.services = [{ name: 'Dia siguiente', value: 'next_day' }];
        break;
      case 'Aeroflash':
        this.services = [
          { name: 'Terrestre', value: 'terrestre' }
        ];
        break;
      case 'Estafeta':
        this.services = [
          {
            name: 'Día Siguiente',
            value: 'next_day'
          },
          {
            name: 'Terrestre',
            value: 'terrestre'
          },
        ];
        break;
    }
  }

  sendGuide() {
    if (this.guide.valid) {
      this.quoteService
        .getQuote(this.guide.getRawValue())
        .subscribe(
          res => {
            this.response = res;
            if (this.response.result[0].price) {
              this.prices = Object.keys(this.response.result[0].price);
            }
            console.log(res);
          },
          error => {
            console.log(error);
          }
        );
    }
  }

  returnService(data) {
    const arr = [
      {
        name: 'Día Siguiente',
        value: '1377731'
      },
      {
        name: 'Terrestre',
        value: '8619166'
      }
    ];

    return arr.filter( service => {
      if (service.value === data) {
        return service;
      }
    })[0].name;
  }
}
