import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatStepperModule } from '@angular/material/stepper';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material';
import { MatInputModule } from '@angular/material';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { HttpClientModule } from '@angular/common/http';
import { MatRadioModule } from '@angular/material/radio';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { Angular2FontawesomeModule } from 'angular2-fontawesome/angular2-fontawesome';
import { MatSelectModule } from '@angular/material/select';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { MatDividerModule } from '@angular/material/divider';
import { PdfViewerModule } from 'ng2-pdf-viewer';

// services
import { LocationService } from './services/location/location.service';
import { PakkeService } from './services/pakke/pakke.service';
import { EtominService } from './services/etomin/etomin.service';

import { AppComponent } from './app.component';
import { ShipmentFormComponent } from './shipment-form/shipment-form.component';
import { ResumeComponent } from './resume/resume.component';
import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { CheckComponent } from './check/check.component';

const appRoutes: Routes = [
  { path: '', component: ShipmentFormComponent },
  { path: 'registro/:data', component: ShipmentFormComponent },
  { path: 'registro', component: ShipmentFormComponent },
  { path: '**', component: ShipmentFormComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    ShipmentFormComponent,
    ResumeComponent,
    NavbarComponent,
    FooterComponent,
    CheckComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(
      appRoutes
    ),
    MDBBootstrapModule.forRoot(),
    BrowserAnimationsModule,
    MatStepperModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    NgbModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatAutocompleteModule,
    HttpClientModule,
    MatRadioModule,
    MatProgressSpinnerModule,
    MatCardModule,
    MatCheckboxModule,
    Angular2FontawesomeModule,
    MatDividerModule,
    PdfViewerModule
  ],
  schemas: [ NO_ERRORS_SCHEMA ],
  providers: [
    LocationService,
    PakkeService,
    EtominService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
