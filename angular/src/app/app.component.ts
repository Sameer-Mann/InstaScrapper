import { Component, OnInit } from '@angular/core';
import { comment } from './comment';
import { FetchDataService } from './fetch-data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'instaScrapper';
  public data ="";
  public comments: Array<comment> = [];
  public errorMsg="";
  public pageId = 0;
  constructor (private _fetchDataServe: FetchDataService){
  }
  handleNext(val : number,data : string){
    this.pageId += val;
    console.log(this.pageId);
    this.handleLoad({"postId":data,"pageId":this.pageId});
  }
  handleLoad(data : {postId : string,pageId : number}){
    console.log(data.postId);
    this._fetchDataServe.getData(data.postId,data.pageId)
    .subscribe(data => this.comments=data,
               error => this.errorMsg = error);
  }
  ngOnInit(){
  }
}
