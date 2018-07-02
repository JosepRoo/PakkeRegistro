import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class LocationService {

  constructor(private http: HttpClient) { }

  getLocations(inputValue): Observable<any>{
    return this.http.get('https://api.geonames.org/postalCodeLookupJSON?placename='+inputValue+'&country=MX&username=alexpakke');
  }

}
