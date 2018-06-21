import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { of } from 'rxjs/observable/of';
import { catchError, map, tap } from 'rxjs/operators';
import { HttpHeaders } from '@angular/common/http';
import 'rxjs/add/operator/catch';

@Injectable()
export class PakkeService {

  private api: string = "https://seller.pakke.mx/api/v1/";
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    'Accept':​ 'application/json',
    'Authorization': 'NJYc54geWEqW2WDR7BiXoSPk7ThfujFirNKdgISJ2I0Qqb7H7ZrzX7zscR5LKcIl'
  });

  constructor(
    private http: HttpClient
  ) { }

  getRates(data): Observable<any> {
    return this.http.post<any>(this.api+'Shipments/rates', data, {headers: this.headers})
      .pipe(map(res => {
            return res.Pakke;
      }))
      .catch(e => {
          if (e.status === 401) {
              return Observable.throw('Unauthorized');
          }
          // do any other checking for statuses here
      });
  }

  makeShipment(data):Observable<any> {
    return this.http.post<any>(this.api+'Shipments', data, {headers: this.headers});
  }

  signUpUser(email, name, password):Observable<any> {
    var data = {
      email: email,
      name: name,
      password: password,
      confirm: password
    }
    return this.http.post<any>(this.api+'Users/signUp', data, {headers: this.headers});
  }



}
