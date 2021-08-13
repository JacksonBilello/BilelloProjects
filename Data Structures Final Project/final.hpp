#ifndef FINAL_HPP
#define HASH_HPP

#include <vector>
#include <iostream>
#include <string>
using namespace std;

#define TABLE_SIZE 10009        //define table size

struct Node   //struct for every value we enter into data structure
{
  int key;
  Node* next;     //LL
  Node* left;     //BST
  Node* right;    //BST
};

class Hash
{
  int tablesize;  //for first table constructor
  int tablesize1;   //for second table constructor
  Node* *tables;    //initialize first table
  Node* *tables1;  //initialize second tabe

  public:
    int Hash1(int key);
    int Hash2(int key);                   //hash functions

    void insertLL(int index, int key);
    Node* searchLL(int index, int key);       //linked list hashing
    void deleteLL(int index, int key);

    void insertBST(int index, int key);
    Node* insertBSTHelper(Node* curr, int key);//insert BST helper
    Node* searchBST(int index, int key);                          //BST hashng
    Node* searchBSTHelper(Node* curr, int key);//search BST helper
    void deleteBST(int index, int key);

    void insertLP(int index, int key);
    Node* searchLP(int index, int key);                   //linear probing hashing
    void deleteLP(int index, int key);

    void insertCH(int index1, int index2, int key);
    Node* searchCH(int index1, int index2, int key);      //cuckoo hashing
    void deleteCH(int index1, int index2, int key);

    Node* getMinValueNode(Node* curr);    //helper function for BST delete
    Hash(); //cst
    ~Hash();  //dst
    Node* createNode(int key);  //creating new node to insert to table
};
#endif
