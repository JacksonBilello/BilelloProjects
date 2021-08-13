//done

#include "final.hpp"
#include<vector>
#include<iostream>
#include<fstream>
#include<string>
#include<limits.h>
#include<climits>
#include<stack>
#include<queue>
#include<list>
#include<ctime>
using namespace std;


int main(int argc, char* argv[]){   //two files are command line
if(argc < 3){
  cout << "not enough inputs" << endl;    //not inputing the two data sets
  return 0;
}

ifstream iFile;       //input file 1
iFile.open(argv[1]);  //open 1

if(!iFile.is_open()){
  cout << "File failed to open" << endl;  //if file cant open return
  return 0;
}

Hash ht;

int startTime, endTime;
double insertH1BST;
startTime = clock();                                      //start time==================
//
string num;
int key;                                    //hash 1 LL insert
int in = 0;  //number of nodes entered into the table
while(getline(iFile, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.
  key = stoi(num);                            //convert to int
  int index = ht.Hash1(key);                         //get the index from hash function
  ht.insertBST(index, key);                           //insert into the table using LL mech
  in++;                                           //+1 added to the table
}
//
endTime = clock();                                          //end time====================
insertH1BST = (double) (endTime-startTime)/100;
cout << "execution time for hash 1, BST insert, LF=0 : " << insertH1BST << endl;
iFile.close();
iFile.open(argv[1]);  //open 1


double searchH1BST;
startTime = clock();
//
int search = 0;
while(getline(iFile, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1                //get a number from the table
  key = stoi(num);                            //convert to int
  int index = ht.Hash1(key);                         //get the index from hash function
  ht.searchBST(index, key);                           //insert into the table using LL mech
  search++;                                           //+1 added to the table
}
//
endTime = clock();                                          //end time====================
searchH1BST = (double) (endTime-startTime)/100;
cout << "execution time for hash 1, BST search, LF=0 : " << searchH1BST << endl;
iFile.close();
iFile.open(argv[1]);  //open 1

double deleteH1BST;
startTime = clock();
//
int del = 0;
while(getline(iFile, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
                //get a number from the table
  key = stoi(num);                            //convert to int
  int index = ht.Hash1(key);                         //get the index from hash function
  ht.deleteBST(index, key);                           //insert into the table using LL mech
  del++;                                           //+1 added to the table
}
//
endTime = clock();                                          //end time====================
deleteH1BST = (double) (endTime-startTime)/100;
cout << "execution time for hash 1, BST delete, LF=0 : " << deleteH1BST << endl;
iFile.close();
iFile.open(argv[1]);  //open 1



  int count = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && count!=1000){   //while we are still adding and the LF isnt 0.1               //0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  iFile.close();
  iFile.open(argv[1]);
  cout << endl;

  //double insertH1BST;
  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',')&& in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.1 : " << insertH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);



  //double searchH1BST;
  startTime = clock();
  //
  search = 0;
  while(getline(iFile, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.1 : " << searchH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  //double deleteH1BST;
  startTime = clock();
  //
  del = 0;
  while(getline(iFile, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.1 : " << deleteH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  count = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && count!=1000){   //while we are still adding and the LF isnt 0.2           //0.2
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  iFile.close();
  iFile.open(argv[1]);
  cout << endl;




  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.2 : " << insertH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  //double searchH1BST;
  startTime = clock();
  //
  search = 0;
  while(getline(iFile, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.2 : " << searchH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  //double deleteH1BST;
  startTime = clock();
  //
  del = 0;
  while(getline(iFile, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.2 : " << deleteH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  count = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && count!=3000){   //while we are still adding and the LF isnt 0.2           //0.5
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  iFile.close();
  iFile.open(argv[1]);
  cout << endl;



  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.5 : " << insertH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  startTime = clock();
  //
  search = 0;
  while(getline(iFile, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.5 : " << searchH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  startTime = clock();
  //
  del = 0;
  while(getline(iFile, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.5 : " << deleteH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);



  count = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && count!=2000){   //while we are still adding and the LF isnt 0.2           //0.7
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  iFile.close();
  iFile.open(argv[1]);
  cout << endl;



  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.7 : " << insertH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  startTime = clock();
  //
  search = 0;
  while(getline(iFile, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.7 : " << searchH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  startTime = clock();
  //
  del = 0;
  while(getline(iFile, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.7 : " << deleteH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);



  count = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && count!=2000){   //while we are still adding and the LF isnt 0.2           //0.9
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  iFile.close();
  iFile.open(argv[1]);
  cout << endl;

  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.9 : " << insertH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  startTime = clock();
  //
  search = 0;
  while(getline(iFile, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.9 : " << searchH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);

  startTime = clock();
  //
  del = 0;
  while(getline(iFile, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.9 : " << deleteH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);

  count = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && count!=1000){   //while we are still adding and the LF isnt 0.2           //1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  iFile.close();
  iFile.open(argv[1]);
  cout << endl;


  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(iFile, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=1 : " << insertH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  startTime = clock();
  //
  search = 0;
  while(getline(iFile, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=1 : " << searchH1BST << endl;
  iFile.close();
  iFile.open(argv[1]);


  startTime = clock();
  //
  del = 0;
  while(getline(iFile, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=1 : " << deleteH1BST << endl;
  iFile.close();
  cout << endl;









  ifstream File;
  File.open(argv[2]);
  if(!File.is_open()){                                                      //data set 2
    cout << "File failed to open" << endl;  //if file cant open return
    return 0;
  }



  startTime = clock();                                      //start time==================
  //                                   //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0 : " << insertH1BST << endl;
  File.close();
  File.open(argv[2]);  //open 1




  startTime = clock();
  //
  search = 0;
  while(getline(File, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1                //get a number from the table
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0 : " << searchH1BST << endl;
  File.close();
  File.open(argv[2]);  //open 1



  startTime = clock();
  //
  del = 0;
  while(getline(File, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
                  //get a number from the table
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0 : " << deleteH1BST << endl;
  File.close();
  File.open(argv[2]);  //open 1




  count = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && count!=1000){   //while we are still adding and the LF isnt 0.1               //0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  File.close();
  File.open(argv[2]);
  cout << endl;


  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(File, num, ',')&& in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.1 : " << insertH1BST << endl;
  File.close();
  File.open(argv[2]);



  //double searchH1BST;
  startTime = clock();
  //
  search = 0;
  while(getline(File, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.1 : " << searchH1BST << endl;
  File.close();
  File.open(argv[2]);


  //double deleteH1BST;
  startTime = clock();
  //
  del = 0;
  while(getline(File, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.1 : " << deleteH1BST << endl;
  File.close();
  File.open(argv[2]);



  count = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && count!=1000){   //while we are still adding and the LF isnt 0.2           //0.2
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  File.close();
  File.open(argv[2]);
  cout << endl;


  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.2 : " << insertH1BST << endl;
  File.close();
  File.open(argv[2]);


  //double searchH1BST;
  startTime = clock();
  //
  search = 0;
  while(getline(File, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.2 : " << searchH1BST << endl;
  File.close();
  File.open(argv[2]);


  //double deleteH1BST;
  startTime = clock();
  //
  del = 0;
  while(getline(File, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.2 : " << deleteH1BST << endl;
  File.close();
  File.open(argv[2]);





  count = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && count!=3000){   //while we are still adding and the LF isnt 0.2           //0.5
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  File.close();
  File.open(argv[2]);
  cout << endl;





  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.5 : " << insertH1BST << endl;
  File.close();
  File.open(argv[2]);


  startTime = clock();
  //
  search = 0;
  while(getline(File, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.5 : " << searchH1BST << endl;
  File.close();
  File.open(argv[2]);


  startTime = clock();
  //
  del = 0;
  while(getline(File, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.5 : " << deleteH1BST << endl;
  File.close();
  File.open(argv[2]);






  count = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && count!=2000){   //while we are still adding and the LF isnt 0.2           //0.7
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  File.close();
  File.open(argv[2]);
  cout << endl;




  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.7 : " << insertH1BST << endl;
  File.close();
  File.open(argv[2]);


  startTime = clock();
  //
  search = 0;
  while(getline(File, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.7 : " << searchH1BST << endl;
  File.close();
  File.open(argv[2]);


  startTime = clock();
  //
  del = 0;
  while(getline(File, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.7 : " << deleteH1BST << endl;
  File.close();
  File.open(argv[2]);





  count = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && count!=2000){   //while we are still adding and the LF isnt 0.2           //0.9
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  File.close();
  File.open(argv[2]);
  cout << endl;






  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=0.9 : " << insertH1BST << endl;
  File.close();
  File.open(argv[2]);


  startTime = clock();
  //
  search = 0;
  while(getline(File, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=0.9 : " << searchH1BST << endl;
  File.close();
  File.open(argv[2]);



  startTime = clock();
  //
  del = 0;
  while(getline(File, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=0.9 : " << deleteH1BST << endl;
  File.close();
  File.open(argv[2]);



  count = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && count!=1000){   //while we are still adding and the LF isnt 0.2           //1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    count++;                                        //+1 added to the table
  }
  File.close();
  File.open(argv[2]);
  cout << endl;



  startTime = clock();                                      //start time==================
  //                                                      //hash 1 LL insert
  in = 0;  //number of nodes entered into the table
  while(getline(File, num, ',') && in != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.insertBST(index, key);                           //insert into the table using LL mech
    in++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  insertH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST insert, LF=1 : " << insertH1BST << endl;
  File.close();
  File.open(argv[2]);


  startTime = clock();
  //
  search = 0;
  while(getline(File, num, ',') && search != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.searchBST(index, key);                           //insert into the table using LL mech
    search++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  searchH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST search, LF=1 : " << searchH1BST << endl;
  File.close();
  File.open(argv[2]);


  startTime = clock();
  //
  del = 0;
  while(getline(File, num, ',') && del != 100){   //while we are still adding and the LF isnt 0.1
    key = stoi(num);                            //convert to int
    int index = ht.Hash1(key);                         //get the index from hash function
    ht.deleteBST(index, key);                           //insert into the table using LL mech
    del++;                                           //+1 added to the table
  }
  //
  endTime = clock();                                          //end time====================
  deleteH1BST = (double) (endTime-startTime)/100;
  cout << "execution time for hash 1, BST delete, LF=1 : " << deleteH1BST << endl;
  File.close();



return 0;
}
