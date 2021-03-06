import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { LocationService } from '../services/location/location.service';
import { PakkeService } from '../services/pakke/pakke.service';
import { AbstractControl, ValidatorFn } from '@angular/forms';
import { PasswordValidation } from './password-validation';
import { MatIconRegistry, MatStepper } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';
import { CreditCardValidator } from 'ngx-credit-cards';
import { environment } from '../../environments/environment';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { ElementRef } from '@angular/core';

// services
import { EtominService } from '../services/etomin/etomin.service';

@Component({
  selector: 'app-shipment-form',
  templateUrl: './shipment-form.component.html',
  styleUrls: ['./shipment-form.component.scss']
})
export class ShipmentFormComponent implements OnInit, AfterViewInit {
  isLinear;
  guide: FormGroup;
  service: FormGroup;
  data: FormGroup;
  payment: FormGroup;
  locations: any[];
  rates: any[];
  calculatingRates: boolean = false;
  months: any;
  years: any;
  loading: boolean = false;
  error: boolean = false;
  shipmentError = false;
  shipmentSaved = false;
  shipment:any;
  pakkeResponse: any;
  stepper: MatStepper;
  editable = true;
  @ViewChild('stepper') step: MatStepper;
  @ViewChild('nextStepButton') nextButton: ElementRef;

  constructor(
    private _formBuilder: FormBuilder,
    private locationService: LocationService,
    private pakkeService: PakkeService,
    private iconRegistry: MatIconRegistry,
    private sanitizer: DomSanitizer,
    private etomin: EtominService,
    private activatedRoute: ActivatedRoute
  ) {
    this.iconRegistry
      .addSvgIcon(
        'mastercard',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/mastercard.svg')
      )
      .addSvgIcon(
        'visa',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/visa.svg')
      )
      .addSvgIcon(
        'amex',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/amex.svg')
      )
      .addSvgIcon(
        'box',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/icn_box.svg')
      )
      .addSvgIcon(
        'company',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/icn_building.svg')
      )
      .addSvgIcon(
        'calendar',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/calendar.svg')
      )
      .addSvgIcon(
        'mexico',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/mexico.svg')
      )
      .addSvgIcon(
        'one',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/one.svg')
      )
      .addSvgIcon(
        'two',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/two.svg')
      )
      .addSvgIcon(
        'three',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/three.svg')
      )
      .addSvgIcon(
        'four',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/four.svg')
      )
      .addSvgIcon(
        'one-active',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/one-active.svg')
      )
      .addSvgIcon(
        'two-active',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/two-active.svg')
      )
      .addSvgIcon(
        'three-active',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/three-active.svg')
      )
      .addSvgIcon(
        'four-active',
        sanitizer.bypassSecurityTrustResourceUrl('./assets/four-active.svg')
      );
  }

  ngOnInit() {
    // months options for the credit card expiration
    this.months = [
      '01',
      '02',
      '03',
      '04',
      '05',
      '06',
      '07',
      '08',
      '09',
      '10',
      '11',
      '12'
    ];

    // generates the next 8 years from now for the credit card  expiration
    var today = new Date();
    var todayYear = today.getFullYear() - 2000;
    this.years = [];
    for (var i = 0; i < 8; i++) {
      this.years.push(String(todayYear));
      todayYear++;
    }

    // guide data form
    this.guide = this._formBuilder.group({
      origin: [
        '',
        Validators.compose([Validators.required]),
        this.validPostalCode(this.locationService)
      ],
      destiny: [
        '',
        Validators.compose([Validators.required]),
        this.validPostalCode(this.locationService)
      ],
      weight: ['', [Validators.required, this.validateMeasure]],
      width: ['', [Validators.required, this.validateMeasure]],
      height: ['', [Validators.required, this.validateMeasure]],
      deep: ['', [Validators.required, this.validateMeasure]],
      valid: ['', Validators.required],
      insuredAmount: ['', Validators.pattern('^[0-9]*')]
    });

    // service form
    this.service = this._formBuilder.group({
      service: ['', Validators.required]
    });

    this.data = this._formBuilder.group(
      {
        name: ['', Validators.required],
        lastName: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        package: ['', Validators.required],
        register: [''],
        password: [
          '',
          [
            Validators.minLength(8),
            Validators.pattern(
              '(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$@$!%*?&])[A-Za-zd$@$!%*?&].{8,}'
            )
          ]
        ],
        confirmPassword: [''],
        originName: ['', Validators.required],
        originCompany: [''],
        originPhone: [
          '',
          [Validators.required, Validators.pattern('[0-9]{10}')]
        ],
        originEmail: ['', [Validators.required, Validators.email]],
        originZipCode: [{ disabled: true }, Validators.required],
        originState: [{ disabled: true }, Validators.required],
        originCity: [{ disabled: true }, Validators.required],
        originColony: [{ disabled: true }, Validators.required],
        originStreet: ['', Validators.required],
        originReferences: ['', Validators.required],
        destinyName: ['', Validators.required],
        destinyCompany: [''],
        destinyPhone: [
          '',
          [Validators.required, Validators.pattern('[0-9]{10}')]
        ],
        destinyEmail: ['', [Validators.required, Validators.email]],
        destinyZipCode: [{ disabled: true }, Validators.required],
        destinyState: [{ disabled: true }, Validators.required],
        destinyCity: [{ disabled: true }, Validators.required],
        destinyColony: [{ disabled: true }, Validators.required],
        destinyStreet: ['', Validators.required],
        destinyReferences: ['', Validators.required],
        confirm: ['', Validators.required],
        conditions: ['', Validators.required]
      },
      {
        validator: PasswordValidation.MatchPassword
      }
    );

    this.payment = this._formBuilder.group(
      {
        name: ['', Validators.required],
        zipCode: ['', [Validators.required, Validators.pattern('[0-9]{5}')]],
        number: [
          '',
          [Validators.required, CreditCardValidator.validateCardNumber]
      ],
        cvv: ['', [Validators.required, CreditCardValidator.validateCardCvc]],
        month: ['', [Validators.required, Validators.pattern('[0-9]{2}')]],
        year: ['', [Validators.required, Validators.pattern('[0-9]{2}')]],
        type: ['', [Validators.required]],
        session: [''],
        reference: [''],
        merchant: [''],
        order: [''],
        transaction: [''],
        token: [''],
        authorization: ['']
      },
      {}
    );

    if (this.activatedRoute.snapshot.params['data']) {
      this.isLinear = false;
      const data = JSON.parse(this.activatedRoute.snapshot.params['data'].replace(/\>/gi, ')').replace(/\</gi, '('));
      console.log(data);
      this.guide.controls.origin.setValue(data.origin);
      this.guide.controls.destiny.setValue(data.destiny);
      this.guide.controls.weight.setValue(data.weight);
      this.guide.controls.height.setValue(data.height);
      this.guide.controls.width.setValue(data.width);
      this.guide.controls.deep.setValue(data.deep);
      if (data.insuredAmount) {
        this.guide.controls.insuredAmount.setValue(data.insuredAmount);
      } else {
        this.guide.controls.insuredAmount.setValue('');
      }
    } else {
      this.isLinear = true;
    }
  }

  ngAfterViewInit() {
    if (this.activatedRoute.snapshot.params['data']) {
      this.guide.controls.valid.setValue(true);
      this.step.next();
      this.step.next();
      this.isLinear = true;
      this.getRatesWithoutValidation(this.step);
    }
  }

  getCardType() {
    var digit = this.payment.controls.number.value[0];
    var cardType = this.payment.controls.type;
    switch (digit) {
      case '5': {
        cardType.setValue('MASTERCARD');
        break;
      }
      case '4': {
        cardType.setValue('VISA');
        break;
      }
      case '3': {
        cardType.setValue('AMEX');
        break;
      }
    }
  }

  validPostalCode(httpService: LocationService) {
    return control =>
      new Promise((resolve, reject) => {
        return httpService
          .getLocations(control.value.substring(0, 6))
          .subscribe(res => {
            return res.postalcodes.length
              ? resolve(null)
              : resolve({ valid: { valid: true } });
          });
      });
  }

  validateMeasure(formControl: FormControl) {
    let number = /^[.\d]+$/.test(formControl.value) ? +formControl.value : NaN;
    if (number !== number) {
      return { value: true };
    }
    if (number <= 0) {
      return { value: true };
    }
    return null;
  }

  autocompleteLocations(inputValue) {
    var self = this;
    return this.locationService
      .getLocations(inputValue)
      .subscribe(locations => {
        if (locations.postalcodes.length)
          self.locations = locations.postalcodes;
      });
  }

  selectService(service, stepper: MatStepper) {
    this.service.controls.service.setValue(service);
    this.data.controls.originZipCode.reset({
      value: this.guide.controls.origin.value.replace(/\s/g, '').substring(0, 5),
      disabled: true
    });
    this.data.controls.originState.reset({
      value: this.guide.controls.origin.value
        .split('(')
        [this.guide.controls.origin.value.split('(').length - 1].substring(
          0,
          3
        ),
      disabled: true
    });
    this.data.controls.originCity.reset({
      value: this.guide.controls.origin.value.split(' - ')[2],
      disabled: true
    });
    this.data.controls.originColony.reset({
      value: this.guide.controls.origin.value.split(' - ')[1],
      disabled: true
    });
    this.data.controls.destinyZipCode.reset({
      value: this.guide.controls.destiny.value
        .replace(/\s/g, '')
        .substring(0, 5),
      disabled: true
    });
    this.data.controls.destinyState.reset({
      value: this.guide.controls.destiny.value
        .split('(')
        [this.guide.controls.destiny.value.split('(').length - 1].substring(
          0,
          3
        ),
      disabled: true
    });
    this.data.controls.destinyCity.reset({
      value: this.guide.controls.destiny.value.split(' - ')[2],
      disabled: true
    });
    this.data.controls.destinyColony.reset({
      value: this.guide.controls.destiny.value.split(' - ')[1],
      disabled: true
    });
    stepper.next();
  }

  getRates(stepper: MatStepper) {
    this.guide.controls.valid.setValue(true);
    if (this.guide.valid) {
      this.calculatingRates = true;
      var data = {
        Parcel: {
          Height: this.guide.controls.height.value,
          Length: this.guide.controls.deep.value,
          Weight: this.guide.controls.weight.value,
          Width: this.guide.controls.width.value
        },
        ZipCodeFrom: this.guide.controls.origin.value.substring(0, 5),
        ZipCodeTo: this.guide.controls.destiny.value.substring(0, 5),
        InsuredAmount: this.guide.controls.insuredAmount.value
      };
      this.pakkeService.getRates(data).subscribe(res => {
        this.rates = res;
        this.calculatingRates = false;
      });
      stepper.next();
    } else {
      this.guide.controls.valid.setValue(null);
    }
  }

  getRatesWithoutValidation(stepper: MatStepper) {
    this.guide.controls.valid.setValue(true);
    const params = JSON.parse(this.activatedRoute.snapshot.params['data'].replace(/\>/gi, ')').replace(/\</gi, '('));
    var data = {
      Parcel: {
        Height: this.guide.controls.height.value,
        Length: this.guide.controls.deep.value,
        Weight: this.guide.controls.weight.value,
        Width: this.guide.controls.width.value
      },
      ZipCodeFrom: this.guide.controls.origin.value.substring(1, 6),
      ZipCodeTo: this.guide.controls.destiny.value.substring(1, 6),
      InsuredAmount: this.guide.controls.insuredAmount.value
    };
    this.pakkeService.getRates(data).subscribe(res => {
      this.rates = res;
      const ser = res.filter(el => {
        // console.log(el);
        // console.log(data);
        return el.CourierServiceId === params.service.CourierServiceId;
      });
      stepper.next();
      this.selectService(ser[0], this.step);
    });
  }

  setEstimatedDate(days) {
    var now = new Date();
    now.setDate(now.getDate() + Number(days));
    return now;
  }

  generateSession(stepper) {
    this.stepper = stepper;
    var self = this;
    if (this.payment.valid) {
      this.loading = true;
      this.error = false;
      this.registerUser();
      this.etomin.getSessionId().subscribe(
        res => {
          self.payment.controls.session.setValue(res.session_id);
          self.payment.controls.merchant.setValue(res.merchant_id);
          self.payment.controls.reference.setValue(self.generateReference());
        },
        error => console.log(error),
        function() {
          self.generateShipment();
        }
      );
    }
  }

  generateReference() {
    var text = '';
    var possible = '0123456789';
    var today = new Date();

    for (var i = 0; i < 3; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));

    return Number(today) + text;
  }

  makePayment() {
    var paymentData = {
      test: false,
      public_key: environment.etominKey,
      transaction: {
        device_session_id: this.payment.controls.session.value,
        order: {
          description: 'Generacion de guia en Pakke',
          external_reference: this.payment.controls.reference.value
        },
        payer: {
          firstName: this.data.controls.name.value,
          lastName: this.data.controls.lastName.value,
          email: this.data.controls.email.value,
          shippingAddress: {
            description: 'Direccion de envio de paquetes',
            street_name: this.data.controls.destinyStreet.value,
            street_number: this.data.controls.destinyReferences.value,
            neighbour: this.data.controls.destinyColony.value,
            city: this.data.controls.destinyCity.value,
            state: this.data.controls.destinyState.value,
            zipcode: this.data.controls.destinyZipCode.value,
            address_type: 1,
            country: 'MX'
          },
          billingAddress: {
            description: 'Direccion de envio de paquetes',
            street_name: this.data.controls.originStreet.value,
            street_number: this.data.controls.originReferences.value,
            neighbour: this.data.controls.originColony.value,
            city: this.data.controls.originCity.value,
            state: this.data.controls.originState.value,
            zipcode: this.data.controls.originZipCode.value,
            address_type: 1,
            country: 'MX'
          }
        },
        payment: {
          amount: this.service.controls.service.value.TotalPrice,
          currency: 'MXN',
          payment_country: 'MEX',
          payment_method: this.payment.controls.type.value,
          number: this.payment.controls.number.value,
          securityCode: this.payment.controls.cvv.value,
          expirationDate:
            this.payment.controls.month.value +
            '/' +
            this.payment.controls.year.value,
          name: this.payment.controls.name.value
        }
      }
    };
    this.etomin.makePayment(paymentData).subscribe(
      res => {
        if (Number(res.error) === 0) {
          this.payment.controls.order.setValue(res.order);
          this.payment.controls.transaction.setValue(res.transaction);
          this.payment.controls.authorization.setValue(res.authorization_code);
          this.payment.controls.token.setValue(res.card_token);
          this.shipmentSaved = false;
          this.pakkeResponse = this.shipment;
          this.stepper.next();
        } else {
          this.error = true;
          this.loading = false;
        }
      },
      error => {
        this.error = true;
        this.loading = false;
      }
    );
  }

  generateShipment() {
    console.log(this.data.controls.originZipCode.value);
    console.log(this.data.controls.originZipCode.value.replace(/\s/g, ''));
    this.error = false;
    this.shipmentError = false;
    if (!this.shipmentSaved) {
      var shipmentData = {
        CourierCode: this.service.controls.service.value.CourierCode,
        CourierServiceId: this.service.controls.service.value.CourierServiceId,
        ServiceTypeCode: this.service.controls.service.value.PakkeServiceCode,
        ResellerReference: this.payment.controls.reference.value,
        AddressFrom: {
          ZipCode: this.data.controls.originZipCode.value.replace(/\s/g, ''),
          State: 'MX-' + this.data.controls.originState.value,
          City: this.data.controls.originCity.value,
          Neighborhood: this.data.controls.originColony.value.substr(0, 34),
          Address1: this.data.controls.originStreet.value,
          Address2: this.data.controls.originReferences.value,
          Residential: this.data.controls.originCompany.value ? false : true
        },
        AddressTo: {
          ZipCode: this.data.controls.destinyZipCode.value.replace(/\s/g, ''),
          State: 'MX-' + this.data.controls.destinyState.value,
          City: this.data.controls.destinyCity.value,
          Neighborhood: this.data.controls.destinyColony.value.substr(0, 34),
          Address1: this.data.controls.destinyStreet.value,
          Address2: this.data.controls.destinyReferences.value,
          Residential: this.data.controls.destinyCompany.value ? false : true
        },
        Parcel: {
          Length: this.guide.controls.deep.value,
          Width: this.guide.controls.width.value,
          Height: this.guide.controls.height.value,
          Weight: this.guide.controls.weight.value
        },
        Sender: {
          Name: this.data.controls.originName.value,
          CompanyName: this.data.controls.originCompany.value,
          Phone1: this.data.controls.originPhone.value,
          Email: this.data.controls.originEmail.value
        },
        Recipient: {
          Name: this.data.controls.destinyName.value,
          CompanyName: this.data.controls.destinyCompany.value,
          Phone1: this.data.controls.destinyPhone.value,
          Email: this.data.controls.destinyEmail.value
        }
      };
      var self = this;
      this.pakkeService.makeShipment(shipmentData).subscribe(res => {
        self.loading = false;
        self.shipment = res;
        self.editable = false;
        self.error = false;
        self.shipmentSaved = true;
        self.makePayment();
      },
      err =>{
        self.shipmentError = err.error.error.details[0];
        self.loading = false;
      });
    } else {
      this.makePayment();
    }
  }

  registerUser() {
    if (this.data.controls.register.value) {
      this.pakkeService
        .signUpUser(
          this.data.controls.email.value,
          this.data.controls.name.value +
            ' ' +
            this.data.controls.lastName.value,
          this.data.controls.password.value
        )
        .subscribe(res => {});
    }
  }
}

//
// ShipmentId	aed4088c-5aca-4c6d-b99d-57d2177f1b60
// CourierCode	DHL
// ResellerId	e6f43b43-7c9d-42fb-afdb-5126548c74ff
// OwnerId	4e5e6494-5656-4919-8db4-1bfd258e97d7
// ResellerReference	REF-DWGZRLKGV173UQF
// TrackingNumber	6294617803
// Status	SUCCESS
// CreatedAt	2018-06-06T13:14:34.938
// UpdatedAt	2018-06-06T13:14:34.939
// HasExceptions	false
// CourierServiceId	DHL_DIA_SIGUIENTE
// AddressFrom	{…}
// ZipCode	11950
// State	MX-CMX
// UserState	MX-CMX
// City	Miguel Hidalgo
// Neighborhood	Lomas Altas
// Address1	Av Constituyentes 908
// Address2	A un lado de Expanción
// Residential	false
// AddressTo	{…}
// ZipCode	53126
// State	MX-MEX
// UserState	MX-MEX
// City	Naucalpan de Juárez (MEX)
// Neighborhood	Lomas Verdes 5a Sección (La Concor
// Address1	calle destino
// Address2	ref destino
// Residential	false
// Parcel	{…}
// Length	1
// Width	1
// Height	1
// Weight	1
// VolumetricWeight	0
// Sender	{…}
// Name	soporte
// CompanyName	pakke
// Phone1	5526299848
// Phone2	5526299848
// Email	contacto@pakke.mx
// Recipient	{…}
// Name	Destino Nombre
// CompanyName	Empres destino
// Phone1	5555555555
// Email	destino@ejemplo.com
// ShipmentDetailId	0ef397a7-06aa-4bad-8262-e0f406d0d90d
// Label	JVBERi0xLjQKJeLjz9MKMiAwIG9iago8PC9MZW5ndGggNTEvRmlsdGVyL0ZsYXRlRGVjb2RlPj5zdHJlYW0KeJwr5HIK4TJQMLU01TOyUAhJ4XIN4QrkKlQwVDAAQgiZnKugH5FmqOCSrxDIBQD9oQpWCmVuZHN0cmVhbQplbmRvYmoKNCAwIG9iago8PC9CYXNlRm9udC9IZWx2ZXRpY2EtQm9sZC9UeXBlL0ZvbnQvRW5jb2RpbmcvV2luQW5zaUVuY29kaW5nL1N1YnR5cGUvVHlwZTE+PgplbmRvYmoKNSAwIG9iago8PC9CYXNlRm9udC9IZWx2ZXRpY2EvVHlwZS9Gb250L0VuY29kaW5nL1dpbkFuc2lFbmNvZGluZy9TdWJ0eXBlL1R5cGUxPj4KZW5kb2JqCjMgMCBvYmoKPDwvVHlwZS9YT2JqZWN0L1Jlc291cmNlczw8L1Byb2NTZXRbL1BERi9UZXh0L0ltYWdlQi9JbWFnZUMvSW1h…G4gCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDMxMyAwMDAwMCBuIAowMDAwMDAwMTMyIDAwMDAwIG4gCjAwMDAwMDAyMjUgMDAwMDAgbiAKMDAwMDAwODU4NCAwMDAwMCBuIAowMDAwMDA4NDIyIDAwMDAwIG4gCjAwMDAwMDQ5MDEgMDAwMDAgbiAKMDAwMDAwNTIwMSAwMDAwMCBuIAowMDAwMDA1MDE4IDAwMDAwIG4gCjAwMDAwMDUxMTIgMDAwMDAgbiAKMDAwMDAwODY1MyAwMDAwMCBuIAowMDAwMDA4Njk5IDAwMDAwIG4gCnRyYWlsZXIKPDwvUm9vdCAxMiAwIFIvSUQgWzxlMWYwOTQ5MjI5MmYwNzk4ZWE1NmY1MDM3MDZhMWQ4Zj48NjhiYzAwNTRhOTQ0Y2E4NDc4NjAyOGY5ZWQ4MWYzMzU+XS9JbmZvIDEzIDAgUi9TaXplIDE0Pj4Kc3RhcnR4cmVmCjg4MTAKJSVFT0YK
// Contenido de respuesta
// 1
//
// {"ShipmentId":"aed4088c-5aca-4c6d-b99d-57d2177f1b60","CourierCode":"DHL","ResellerId":"e6f43b43-7c9d-42fb-afdb-5126548c74ff","OwnerId":"4e5e6494-5656-4919-8db4-1bfd258e97d7","ResellerReference":"REF-DWGZRLKGV173UQF","TrackingNumber":"6294617803","Status":"SUCCESS","CreatedAt":"2018-06-06T13:14:34.938","UpdatedAt":"2018-06-06T13:14:34.939","HasExceptions":false,"CourierServiceId":"DHL_DIA_SIGUIENTE","AddressFrom":{"ZipCode":"11950","State":"MX-CMX","UserState":"MX-CMX","City":"Miguel Hidalgo","Neighborhood":"Lomas Altas","Address1":"Av Constituyentes 908","Address2":"A un lado de Expanción","Residential":false},"AddressTo":{"ZipCode":"53126","State":"MX-MEX","UserState":"MX-MEX","City":"Naucalpan de Juárez (MEX)","Neighborhood":"Lomas Verdes 5a Sección (La Concor","Address1":"calle destino","Address2":"ref destino","Residential":false},"Parcel":{"Length":1,"Width":1,"Height":1,"Weight":1,"VolumetricWeight":0},"Sender":{"Name":"soporte","CompanyName":"pakke","Phone1":"5526299848","Phone2":"5526299848","Email":"contacto@pakke.mx"},"Recipient":{"Name":"Destino Nombre","CompanyName":"Empres destino","Phone1":"5555555555","Email":"destino@ejemplo.com"},"ShipmentDetailId":"0ef397a7-06aa-4bad-8262-e0f406d0d90d","Label":"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IF0JZM8JAb9iwggRX6AyAulKIHtGcOlVeiU4iVfdlZD1SMj2nKDg/MoJGr84wQikK4HsOQGiDgfYJsUWXQHJnLf3+B0BBgitJ7KuALLnhNh6wssmxxZdCXHfE141OVZBddN4IuuRkO05wbWeoJfOjOBbT2T7SrgsdxjpypbfpuD2cwLzqhnvp12+nivfIHJKRANFpQ+9nry3937/igCf14zX9sqofLOG99XDenf3VPw43y43dw9vB2Q0uLTH24Gs2asVk24e9i9NsLixoVya+HwjcbxcDOu7QZyu5viucnMpbtP1jliuxV2+Ypt8JDPZBdQS+Q7TmEgXXK8Pezgv9fDHOuMc1Fx66n3og9v4fP9o0ivD9AWo4C297z0Qt/i9KonDleKA076Hv/8HBe7oLgplbmRzdHJlYW0KZW5kb2JqCjcgMCBvYmoKPDwvUGFyZW50IDYgMCBSL0NvbnRlbnRzIDggMCBSL1R5cGUvUGFnZS9SZXNvdXJjZXM8PC9YT2JqZWN0PDwvWGYxIDkgMCBSPj4vUHJvY1NldFsvUERGL1RleHQvSW1hZ2VCL0ltYWdlQy9JbWFnZUldPj4vTWVkaWFCb3hbMCAwIDg0MS44OSA1OTUuMjhdPj4KZW5kb2JqCjYgMCBvYmoKPDwvSVRYVCgyLjEuNykvVHlwZS9QYWdlcy9Db3VudCAyL0tpZHNbMSAwIFIgNyAwIFJdPj4KZW5kb2JqCjEyIDAgb2JqCjw8L1R5cGUvQ2F0YWxvZy9QYWdlcyA2IDAgUj4+CmVuZG9iagoxMyAwIG9iago8PC9Qcm9kdWNlcihpVGV4dCAyLjEuNyBieSAxVDNYVCkvTW9kRGF0ZShEOjIwMTgwNjA2MTgxNDM4WikvQ3JlYXRpb25EYXRlKEQ6MjAxODA2MDYxODE0MzhaKT4+CmVuZG9iagp4cmVmCjAgMTQKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDA0NzM5IDAwMDAwIG4gCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDMxMyAwMDAwMCBuIAowMDAwMDAwMTMyIDAwMDAwIG4gCjAwMDAwMDAyMjUgMDAwMDAgbiAKMDAwMDAwODU4NCAwMDAwMCBuIAowMDAwMDA4NDIyIDAwMDAwIG4gCjAwMDAwMDQ5MDEgMDAwMDAgbiAKMDAwMDAwNTIwMSAwMDAwMCBuIAowMDAwMDA1MDE4IDAwMDAwIG4gCjAwMDAwMDUxMTIgMDAwMDAgbiAKMDAwMDAwODY1MyAwMDAwMCBuIAowMDAwMDA4Njk5IDAwMDAwIG4gCnRyYWlsZXIKPDwvUm9vdCAxMiAwIFIvSUQgWzxlMWYwOTQ5MjI5MmYwNzk4ZWE1NmY1MDM3MDZhMWQ4Zj48NjhiYzAwNTRhOTQ0Y2E4NDc4NjAyOGY5ZWQ4MWYzMzU+XS9JbmZvIDEzIDAgUi9TaXplIDE0Pj4Kc3RhcnR4cmVmCjg4MTAKJSVFT0YK"}
