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
    'x-api-key': '7710b94e651b6b1b2de4995cae07f03e6e240a85'
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



}
