import { environment } from '../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { throwError } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class QuoteService {
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(
    private http: HttpClient,
  ) {}

  getQuote(data): Observable<any> {
    return this.http
      .post(environment.url + '/courrier/price', data, {
        headers: this.headers
      })
      .pipe( map(res => {
          return res;
        }), catchError(e => {
          throw e;
        }) );
  }
}
