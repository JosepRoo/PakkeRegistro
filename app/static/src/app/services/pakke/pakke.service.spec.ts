import { TestBed, inject } from '@angular/core/testing';

import { PakkeService } from './pakke.service';

describe('PakkeService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PakkeService]
    });
  });

  it('should be created', inject([PakkeService], (service: PakkeService) => {
    expect(service).toBeTruthy();
  }));
});
