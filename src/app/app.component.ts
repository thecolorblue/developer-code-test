import { Component, OnInit, ViewChild, TemplateRef } from '@angular/core';
import { Observable } from 'rxjs';
import { StringDecoder } from 'string_decoder';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { map } from 'rxjs/operators';

interface Artwork {
  accession_number: string;
  attribution: string;
  created: string;
  creator_description: string;
  creator_lifetime: string;
  creator_name: string;
  creator_region: string;
  creator_role: string;
  department_name: string;
  description: string;
  title: string;
  tombstone: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  $artwork: Observable<Artwork[]>;

  @ViewChild('artworkDialog') artworkDialog: TemplateRef<Artwork>;

  constructor(
    private http: HttpClient,
    private dialog: MatDialog
    ) {}

  ngOnInit() {
    this.$artwork = this.http.get<Artwork[]>('./assets/artwork.json')
      .pipe(map(artwork => {
        // remove duplicates by 'accession_number'
        const unique = [];

        artwork.forEach(current => {
          if (!unique.map(art => art.accession_number).includes(current.accession_number)) {
            unique.push(current);
          }
        });

        return unique;
      }));

    this.$artwork.subscribe(artwork => {
      console.log(artwork);
    });
  }

  openDialog(artwork: Artwork) {
    this.dialog.open<any, { artwork: Artwork }>(this.artworkDialog, {
      data: { artwork },
      maxHeight: 'calc(100vh - 10px)',
    });
  }

  next(current: Artwork, category?: string) {
    this.$artwork.subscribe((artwork: Artwork[]) => {
      let currentIndex;
      let next;
      let list;

      if (category === 'artist') {
        list = artwork.filter(a => a.creator_name === current.creator_name);
      } else if (category === 'department') {
        list = artwork.filter(a => a.department_name === current.department_name);
      } else {
        list = artwork;
      }

      currentIndex = list.map(a => JSON.stringify(a)).indexOf(JSON.stringify(current));

      if (list[currentIndex + 1]) {
        next = list[currentIndex + 1];
      } else {
        next = list[0];
      }
      // sort by category

      // find current artwork

      // find next artwork
      this.dialog.closeAll();
      this.dialog.open<any, { artwork: Artwork }>(this.artworkDialog, {
        data: { artwork: next },
        maxHeight: 'calc(100vh - 10px)',
      });
    });
  }
}
