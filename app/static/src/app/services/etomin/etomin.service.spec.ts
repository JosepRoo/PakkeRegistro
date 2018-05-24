import { TestBed, inject } from '@angular/core/testing';

import { EtominService } from './etomin.service';

describe('EtominService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [EtominService]
    });
  });

  it('should be created', inject([EtominService], (service: EtominService) => {
    expect(service).toBeTruthy();
  }));
});
