import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class WeightService {

  headers: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  constructor(
    private http: HttpClient
  ) { }

  getData(): Observable<any> {
    const data = {
      origin_zipcode: '11200',
      destiny_zipcode: '77500'
    };
    return this.http.post('/courrier/weight', data, {headers: this.headers}).pipe(map(res => {
      return res;
    }));
  }

  print(data): Observable<any> {
    return this.http.post('/package/print', data, { headers: this.headers }).pipe(map(res => {
      return res;
    }));
  }
}
// package/print

// public_price
// pakke_price
// weight
