import {Component, OnInit} from '@angular/core';
import {UserService} from '../user.service';
import {AuthService} from '../auth.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  fileToUpload: File;
  loader = false;
  constructor(private userService: UserService, public auth: AuthService) {
  }

  ngOnInit() {
  }

  changeFile(event) {
    if (event.target.files && event.target.files.length) {
      const file = event.target.files[0];
      this.fileToUpload = file;
    }
  }

  sendFile() {
    this.loader = true;
    this.userService.sendFile(this.fileToUpload).subscribe((res: any) => {
      console.log(res);
      if (res.status === 200) {
        this.loader = false;
      }
    });
  }
}
