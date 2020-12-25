import { Component, OnInit } from '@angular/core';
import { comment } from './comment';
import { FetchDataService } from './fetch-data.service';
import { DomSanitizer } from '@angular/platform-browser';


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
  public imgSrc="";
  public prevId="";
  constructor (private _fetchDataServe: FetchDataService,private sanitize: DomSanitizer){
  }
  handleNext(val : number,data : string){
    if(data != this.prevId){
      this.pageId=0
      this.prevId = data;
    };
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
  loadImage(postId : string){
    this._fetchDataServe.getImage(postId)
    .subscribe(data=>{
      var url:string = JSON.stringify(
        this.sanitize.bypassSecurityTrustUrl(
          JSON.stringify(data)));
      console.log(url);
      this.imgSrc = url;
    });
  }
  ngOnInit(){
  }
}
