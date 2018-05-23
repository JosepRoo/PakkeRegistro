import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { of } from 'rxjs/observable/of';
import { catchError, map, tap } from 'rxjs/operators';
import { HttpHeaders } from '@angular/common/http';
import 'rxjs/add/operator/catch';
import { environment } from '../../../environments/environment';


@Injectable()
export class EtominService {

  private api: string = "https://api.etomin.com/API/v1.0/";
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    'Accept':​ 'application/json'
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

  getSessionId(): Observable<any> {
    return this.http.get<any>(this.api+'kount/auth', {headers: this.headers})
    .pipe(
      map(res => {
        return res;
      })
    )
  }

  makePayment(data): Observable<any>{
    return this.http.post<any>(this.api+'payment', data, {headers: this.headers});
  }





}
