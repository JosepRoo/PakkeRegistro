import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { LocationService } from '../services/location/location.service';
import { PakkeService } from '../services/pakke/pakke.service';
import { AbstractControl, ValidatorFn } from '@angular/forms';
import { PasswordValidation } from './password-validation';
import { MatIconRegistry } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';
import { CreditCardValidator } from 'ngx-credit-cards';
import { environment } from '../../environments/environment';
import { MatStepper } from '@angular/material';

// services
import { EtominService } from '../services/etomin/etomin.service';

@Component({
  selector: 'app-shipment-form',
  templateUrl: './shipment-form.component.html',
  styleUrls: ['./shipment-form.component.css']
})
export class ShipmentFormComponent implements OnInit {
  isLinear                  = true;
  guide: FormGroup;
  service: FormGroup;
  data: FormGroup;
  payment: FormGroup;
  locations: any[];
  rates: any[];
  calculatingRates: boolean = false;
  months : any;
  years : any;
  loading: boolean          = false;
  error: boolean          = false;
  pakkeResponse: any;
  stepper: MatStepper;
  editable = true;

  constructor(
    private _formBuilder   : FormBuilder,
    private locationService: LocationService,
    private pakkeService   : PakkeService,
    private iconRegistry   : MatIconRegistry,
    private sanitizer      : DomSanitizer,
    private etomin         : EtominService,
  ) {

    this.iconRegistry
    .addSvgIcon('mastercard', sanitizer.bypassSecurityTrustResourceUrl('./assets/mastercard.svg'))
    .addSvgIcon('visa', sanitizer.bypassSecurityTrustResourceUrl('./assets/visa.svg'))
    .addSvgIcon('amex', sanitizer.bypassSecurityTrustResourceUrl('./assets/amex.svg'))
  }

  ngOnInit() {

    // months options for the credit card expiration
    this.months = ['01','02','03','04','05','06','07','08','09','10','11','12'];

    // generates the next 8 years from now for the credit card  expiration
    var today = new Date();
    var todayYear = today.getFullYear() - 2000;
    this.years = [];
    for (var i = 0; i < 8; i++ ){
      this.years.push(String(todayYear));
      todayYear++;
    }

    // guide data form
    this.guide = this._formBuilder.group({
      origin : ['', Validators.compose([Validators.required]), this.validPostalCode(this.locationService)],
      destiny: ['', Validators.compose([Validators.required]), this.validPostalCode(this.locationService)],
      weight : ['', [Validators.required, this.validateMeasure]],
      width  : ['', [Validators.required, this.validateMeasure]],
      height : ['', [Validators.required, this.validateMeasure]],
      deep   : ['', [Validators.required, this.validateMeasure]],
      valid : ['', Validators.required]
    });

    // service form
    this.service = this._formBuilder.group({
      service: ['', Validators.required]
    });

    this.data = this._formBuilder.group({
      name             : ['', Validators.required],
      lastName         : ['', Validators.required],
      email            : ['', [Validators.required, Validators.email]],
      package          : ['', Validators.required],
      register         : [''],
      password         : ['', [Validators.minLength(8), Validators.pattern('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&].{8,}')]],
      confirmPassword  : [''],
      originName       : ['', Validators.required],
      originCompany    : [''],
      originPhone      : ['', [Validators.required, Validators.pattern("[0-9]{10}")]],
      originEmail      : ['', Validators.required],
      originZipCode    : [{disabled: true}, Validators.required],
      originState      : [{disabled: true}, Validators.required],
      originCity       : [{disabled: true}, Validators.required],
      originColony     : [{disabled: true}, Validators.required],
      originStreet     : ['', Validators.required],
      originReferences : ['', Validators.required],
      destinyName      : ['', Validators.required],
      destinyCompany   : [''],
      destinyPhone     : ['', [Validators.required, Validators.pattern("[0-9]{10}")]],
      destinyEmail     : ['', Validators.required],
      destinyZipCode   : [{disabled: true}, Validators.required],
      destinyState     : [{disabled: true}, Validators.required],
      destinyCity      : [{disabled: true}, Validators.required],
      destinyColony    : [{disabled: true}, Validators.required],
      destinyStreet    : ['', Validators.required],
      destinyReferences: ['', Validators.required],
      confirm          : ['', Validators.required],
      conditions       : ['', Validators.required],
    }, {
      validator: PasswordValidation.MatchPassword
    });

    this.payment = this._formBuilder.group({
      name         : ['', Validators.required],
      zipCode      : ['', [Validators.required, Validators.pattern("[0-9]{5}")]],
      number       : ['', [Validators.required, CreditCardValidator.validateCardNumber]],
      cvv          : ['', [Validators.required, Validators.pattern("[0-9]{3}")]],
      month        : ['', [Validators.required, Validators.pattern("[0-9]{2}")]],
      year         : ['', [Validators.required, Validators.pattern("[0-9]{2}")]],
      type         : ['', [Validators.required]],
      session      : [''],
      reference    : [''],
      merchant     : [''],
      order        : [''],
      transaction  : [''],
      token        : [''],
      authorization: ['']
    }, {

    });

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
    return control => new Promise((resolve, reject) => {
      return httpService.getLocations(control.value).subscribe(res => {
        return res.postalcodes.length ? resolve(null) : resolve({ valid : { valid: true}});;
      });
    });
  }

  validateMeasure(formControl: FormControl) {
    let number = /^[.\d]+$/.test(formControl.value) ? +formControl.value : NaN;
    if (number !== number) {
      return { 'value': true };
    }
    if (number <= 0){
      return { 'value': true };
    }
    return null;
  }

  autocompleteLocations(inputValue) {
    var self = this;
    return this.locationService.getLocations(inputValue).subscribe(locations => {
      self.locations = locations.postalcodes;
    });
  }

  selectService(service, stepper: MatStepper){
    this.service.controls.service.setValue(service);
    this.data.controls.originZipCode.reset({value : this.guide.controls.origin.value.substring(0,5), disabled: true});
    this.data.controls.originState.reset({value   : this.guide.controls.origin.value.split("(")[this.guide.controls.origin.value.split("(").length - 1].substring(0,3), disabled: true});
    this.data.controls.originCity.reset({value    : this.guide.controls.origin.value.split(" - ")[2], disabled: true});
    this.data.controls.originColony.reset({value  : this.guide.controls.origin.value.split(" - ")[1], disabled: true});
    this.data.controls.destinyZipCode.reset({value: this.guide.controls.destiny.value.substring(0,5), disabled: true});
    this.data.controls.destinyState.reset({value  : this.guide.controls.destiny.value.split("(")[this.guide.controls.destiny.value.split("(").length - 1].substring(0,3), disabled: true});
    this.data.controls.destinyCity.reset({value   : this.guide.controls.destiny.value.split(" - ")[2], disabled: true});
    this.data.controls.destinyColony.reset({value : this.guide.controls.destiny.value.split(" - ")[1], disabled: true});
    stepper.next();
  }

  getRates(stepper: MatStepper){
    this.guide.controls.valid.setValue(true);
    if (this.guide.valid){
      this.calculatingRates = true;
      var data = {
        Parcel: {
          Height: this.guide.controls.height.value,
          Length: this.guide.controls.deep.value,
          Weight: this.guide.controls.weight.value,
          Width: this.guide.controls.width.value
        },
        ZipCode: this.guide.controls.destiny.value.substring(0,5)
      }
      this.pakkeService.getRates(data).subscribe(res => {
        this.rates = res;
        this.calculatingRates = false;
      });
      stepper.next();
    } else {
      this.guide.controls.valid.setValue(null);
    }
  }

  setEstimatedDate(days){
    var now = new Date();
    now.setDate(now.getDate() + Number(days) );
    return now;
  }

  generateSession(stepper) {
    this.stepper = stepper;
    var self = this;
    this.loading = true;
    this.error = false;
    if (this.payment.valid){
      this.registerUser();
      this.etomin.getSessionId().subscribe(
      res => {
        self.payment.controls.session.setValue(res.session_id);
        self.payment.controls.merchant.setValue(res.merchant_id);
        self.payment.controls.reference.setValue(self.generateReference());
      },
      error => console.log(error),
      function() {
        self.makePayment()
      })
    }
  }

  generateReference() {
    var text = "REF-";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

    for (var i = 0; i < 15; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
  }

  makePayment() {
    var paymentData = {
      test: false,
      public_key: environment.etominKey,
      transaction: {
        device_session_id: this.payment.controls.session.value,
        order: {
            description       : "Generacion de guia en Pakke",
            external_reference: this.payment.controls.reference.value,
        },
        payer: {
            firstName  : this.data.controls.name.value,
            lastName   : this.data.controls.lastName.value,
            email      : this.data.controls.email.value,
            shippingAddress: {
                description     : "Direccion de envio de paquetes",
                street_name     : this.data.controls.destinyStreet.value,
                street_number   : this.data.controls.destinyReferences.value,
                neighbour       : this.data.controls.destinyColony.value,
                city            : this.data.controls.destinyCity.value,
                state           : this.data.controls.destinyState.value,
                zipcode         : this.data.controls.destinyZipCode.value,
                address_type    : 1,
                country         : "MX"
            },
            billingAddress: {
              description     : "Direccion de envio de paquetes",
              street_name     : this.data.controls.originStreet.value,
              street_number   : this.data.controls.originReferences.value,
              neighbour       : this.data.controls.originColony.value,
              city            : this.data.controls.originCity.value,
              state           : this.data.controls.originState.value,
              zipcode         : this.data.controls.originZipCode.value,
              address_type    : 1,
              country         : "MX"
            }
        },
        payment: {
          amount         : this.service.controls.service.value.TotalCost,
          currency       : "MXN",
          payment_country: "MEX",
          payment_method : this.payment.controls.type.value,
          number: this.payment.controls.number.value,
          securityCode: this.payment.controls.cvv.value,
          expirationDate: this.payment.controls.month.value +'/'+this.payment.controls.year.value,
          name: this.payment.controls.name.value
        }
      }
    };
    this.etomin.makePayment(paymentData).subscribe(res=>{
      if (Number(res.error) == 0){
        this.payment.controls.order.setValue(res.order);
        this.payment.controls.transaction.setValue(res.transaction);
        this.payment.controls.authorization.setValue(res.authorization_code);
        this.payment.controls.token.setValue(res.card_token);
        this.generateShipment();

      } else {
        this.loading = false;
        this.error = true;
      }
    }, error => {
      this.loading = false;
      this.error = true;
    })
  }

  generateShipment() {
    var shipmentData = {
      CourierCode: this.service.controls.service.value.CourierCode,
      ServiceTypeCode: this.service.controls.service.value.PakkeServiceCode,
      ResellerReference: this.payment.controls.reference.value,
      AddressFrom: {
        ZipCode: this.data.controls.originZipCode.value,
        State: "MX-"+this.data.controls.originState.value,
        City: this.data.controls.originCity.value,
        Neighborhood: this.data.controls.originColony.value,
        Address1: this.data.controls.originStreet.value,
        Address2: this.data.controls.originReferences.value,
        Residential: this.data.controls.originCompany.value ? false : true
      },
      AddressTo: {
        ZipCode: this.data.controls.destinyZipCode.value,
        State: "MX-"+this.data.controls.destinyState.value,
        City: this.data.controls.destinyCity.value,
        Neighborhood: this.data.controls.destinyColony.value,
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
      Sender : {
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
    }
    var self = this;
    this.pakkeService.makeShipment(shipmentData).subscribe(res=>{
      self.loading = false;
      self.error = false;
      self.pakkeResponse = res;
      self.editable = false;
      self.stepper.next();
    })
  }


  createPdf(b64Data) {
    var contentType = 'pdf';
    var sliceSize = 512;

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

    var newWindow = window.open(blobUrl);
  }

  registerUser(){
    if (this.data.controls.register.value){
      this.pakkeService.signUpUser(this.data.controls.email.value, this.data.controls.name.value + " " + this.data.controls.lastName.value, this.data.controls.password.value ).subscribe(res => {});
    }
  }

}
