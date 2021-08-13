#include "final.hpp"
#include<vector>
#include<iostream>
#include<string>
#include<limits.h>
#include<climits>
#include<stack>
#include<queue>
#include<list>
#include<cmath>
using namespace std;


Hash::Hash()      //constructor
{
    this->tablesize= TABLE_SIZE;
    tables = new Node*[tablesize];    //creating new node at each point in the table
    for(int i=0;i<TABLE_SIZE;i++)
    {
        tables[i] = nullptr;        //setting each node equal to null
    }

    this->tablesize1 = TABLE_SIZE;
    tables1 = new Node*[tablesize1];    //creating second table for cuckoo
    for(int i=0; i<TABLE_SIZE;i++)
    {
      tables1[i] = nullptr;         //setting each node to null
    }
}

  void BSTHelper(Node* temp)    //helper function to deconstruct BST
  {
    if(temp->right)
    {
      BSTHelper(temp->right);
    }
    if(temp->left)
    {
        BSTHelper(temp->left);
    }
    delete temp;

  }


  Hash::~Hash()       //deconstructor
  {
    for(int i = 0; i < TABLE_SIZE; i++)
    {
      Node* temp1 = tables[i];
      if(temp1)
      {
        Node* temp2 = temp1->next;
        if(temp1->next) //IF ITS A LINKED LIST
        {
          while(temp1)
          {
            temp2 = temp1->next;
            delete temp1;
            temp1 = temp2;
          }
        }
        else //IF ITS A BST
        {
          BSTHelper(temp1);
        }
      }
    }
    for(int i=0; i<TABLE_SIZE;i++)
    {
      Node* temp = tables1[i];
      delete temp;
    }
  }


Node* Hash::createNode(int key)     //creating a new node to add to data structure
{
    Node* newNode = new Node;   //new node
    newNode->key = key;         //key value for our number
    newNode->left = NULL;       //left child for BST
    newNode->right = NULL;      //right child for BST
    return newNode;     //return new node to use
}

/*
void Hash::destroyNode(Node *currNode){
     if(currNode!=NULL)
     {
         destroyNode(currNode->left);
         destroyNode(currNode->right);

         delete currNode;
         currNode = NULL;
     }
 }
*/

int Hash::Hash1(int key){     //returns the modulus integer for the index
return (key % TABLE_SIZE);
}

int Hash::Hash2(int key){     //returns floor value for the index
  int ind = floor(key/TABLE_SIZE);
return ind;
}

void Hash::insertLL(int index, int key){  //lookup index first
  //at the found index, traverse the LL and place key at the end of the list
  Node* ser = searchLL(index, key);   //finds if our value is already in the LL
  if(ser!=NULL)   //if value is found, we have a duplicate
  {
    //duplicate
  }
  else      //if our value isnt in the list
  {
    Node* newNode = createNode(key);

    Node* curr = tables[index];   //lead pointer to traverse
    Node* trail = NULL;         //trailing pointer to follow
    if(curr==NULL)    //if the LL is empty
    {
      curr=newNode;     //add new node to start position
    }
    else    //if there is a list already
    {
      while(curr!=NULL)   //traverse the list until trail hits last value
      {
        trail = curr;
        curr = curr->next;
      }
      trail->next = newNode;    //add new node to end of the list
  }
}
}//end func

Node* Hash::searchLL(int index, int key){      //lookup index for the key
  Node* curr = tables[index];   //find head of the LL
  Node* trail = NULL;           //set trail node

  if(curr==NULL)    //if the list is empty
  {
    return NULL;    //return null, couldnt find value
  }

  while(curr->key != key && curr!=NULL)   //while we havent found key and havent hit the end of the LL
  {
    trail = curr;       //traverse through
    curr = curr->next;
  }

  if(curr==NULL)    //if we traverse entire list and dont find spot
  {
    return NULL;    //return null, not there
  }

  //at the index, search the LL until you find the key and return true
  //if LL gets to NULL return false
return curr;      //if we didnt return NULL, we found the value and return it
}

void Hash::deleteLL(int index, int key){    //lookup index for the key
  //traverse LL until key is found or NULL is hit, delete the item or finish func
  Node* ser = searchLL(index, key);   //search for value to delete
  if(ser==NULL)   //if we cant find value
  {
    //not in list
  }
  else    //if it is in the list
  {
    Node* curr = tables[index];   //find head of the linked list
    Node* trail = NULL;           //trail node

    if(curr->next == NULL && curr->key==key)    //if only one in the list
    {
      Node* temp = curr;  //delete node and set head equal to NULL
      delete curr;
      temp = NULL;
    }
    else
    {
      while(curr->key != key && curr!=NULL)   //while we havent found key and arent at end of LL
      {
        trail = curr;       //traverse until we find value
        curr = curr->next;
      }

      Node* temp = curr;          //delete the value in the list
      trail->next = temp->next;   //previous node now points to current nodes next
      delete temp;                //delete our node we are looking for
    }
  }
}

Node* Hash::insertBSTHelper(Node* curr, int key){
  if(curr==NULL)    //if we find the correct spot to add node
  {
    return createNode(key);     //create new node
  }
  else if(curr->key < key)    //if key is larger than current key
  {
    curr->right = insertBSTHelper(curr->right, key);    //recursivly go right
  }
  else if(curr->key > key)    //if key is smaller than current key
  {
    curr->left = insertBSTHelper(curr->left, key);  //recursivly go left
  }
  return curr;             //return current value
}

void Hash::insertBST(int index, int key){ //lookup the index of the BST
  //traverse the BST until the correct location is found
  //insert the key in proper location
  Node* ser = searchBST(index, key);  //find if our value is already in BST
  if(ser!=NULL) //if the search finds the key
  {
    //duplicate
  }
  else
  {
    Node* curr = tables[index];     //points to the head of the BST at our insert index
    insertBSTHelper(curr, key);     //send root of BST and key to helper function
  }
}


Node* Hash::searchBSTHelper(Node* curr, int key){
  if(curr==NULL)     //if root is null,
  {
    return NULL;    //return null, couldnt find
  }
  if(curr->key==key)    //if we find our key we are looking for
  {
    return curr;        //return node with our key
  }
  if(curr->key > key)     //if our key is smaller
  {
    return searchBSTHelper(curr->left, key);    //recursivly go left
  }
  if(curr->key < key)     //if our key is bigger
  {
    return searchBSTHelper(curr->right, key);   //recursivly go right
  }
  return curr;      //returning value
}


Node* Hash::searchBST(int index, int key){   //lookup index of BST
  Node* current = tables[index];          //find root of the BST
  Node* tree = searchBSTHelper(current, key);   //send root into the helper function
  if(tree!=NULL)    //if we found our value
  {
    return tree;    //return value we are looking for
  }
  return NULL;      //if we dont find it, return null
}

void Hash::deleteBST(int index, int key){   //lookup index of BST
//traverse the tree until the key is found, delte the node if at a leaf
//if the node is not at a leaf do proper switch then delete the node
Node* curr = searchBST(index, key);   //search for our value in the search tree
if(curr==NULL){   //if it returns NULL
  //not in the tree
}
else    //if it is in the list
{
  //No child / root value case
    Node* root = tables[index];   //find root of BST
    if(curr->left == NULL && curr->right == NULL) //if our value has no children
    {
      if(curr == root)    //if theres only the root, that is our value
      {
        root = curr;    //root becomes our value
        delete curr;    //delete our nnode
        root = NULL;    //make the root null
      }
      else      //if its a leaf node
      {
        delete curr;    //delete the node
      }
    }
    //Only right child
    else if(curr->left == NULL) //if only right child
    {
      Node* temp = curr->right;   //temp is our nodes right node
      curr->key=curr->right->key;   //our nodes key then becomes right child key
      delete temp;                //delete the child node
    }
    //Only left child
    else if(curr->right == NULL)  //if theres only a left child
    {
      Node* temp = curr->left;    //left child is temp
      curr->key=curr->left->key;    //current value becomes left child value
      delete temp;                  //delete the child node
    }
    //Both left and right child
    else
    {
      Node* temp = curr;  //node to be replaced
      curr=curr->right; //go to right sub tree
      Node* newNode = getMinValueNode(curr); //the new node to replace is to the left of the parent
      temp->key=newNode->key; //the original node is replaced with the new node
      delete newNode;       //delete min node
    }
}//big else
}//end func

Node* Hash::getMinValueNode(Node* curr){    //to replace node with 2 children, we need the next biggest node

    if(curr->left == NULL){   //if we found next largest node
      return curr;            //return the node
    }
    return getMinValueNode(curr->left);   //if still smaller nodes, return next left child
  }

void Hash::insertLP(int index, int key){  //lookup initial index
  //if the initial index is empty, insert the key at the index
  //if the index is occupied, increase the index 1 until there is an empty index and insert
  Node* ser = searchLP(index, key); //search if our value is already in the table
  if(ser!=NULL) //if we find our value in the table
  {
    //duplicate
  }
  else
  {
    Node* newNode = createNode(key);  //create new node
    Node* start = tables[index];  //find our initial index
    if(start==NULL) //if the slot is empty
    {
      start = newNode;    //add our node to the index
    }
    else  //if theres something in the index
    {
      index++;  //increment index to next slot
      Node* trav = tables[index]; ///traversing node
      while(trav!=NULL && trav!=start)  //while there isnt an empty slot and we havent looped
      {
        index++;    //increment index by 1
        if(index == TABLE_SIZE+1) //if index gets to the end of the array
        {
          index = 0;    //go back to the start of the array
        }
        trav = tables[index];        //assign new to new index
        if(trav==start)             //if we made a full loop
        {
            //REHASH the table
        }
      }//end while
      if(trav==NULL)  //if we find the next open spot
      {
      trav->key = key;   //enter our key into next open node
      }
    }
}
}

Node* Hash::searchLP(int index, int key){  //lookup the initial index

  //if the index has the key were looking for, return true
  //if the index is not there increase index by one until either the key is found or the index is empty
  Node* start = tables[index];  //find our initial index node
  if(start==NULL)   //if theres nothing in the slot
  {
    return NULL;  //our value isnt in the list
  }
  else if(start->key==key)  //if our value is in initial spot
  {
    return start;   //return our node
    //found
  }
  else      //if we have to traverse nodes
  {
    index++;    //increment index
    Node* trav = tables[index];   //traversing node
    while(trav->key!=key && trav!=NULL) //while our traversing node hasnt found our key or an open spot
    {
      if(trav==start)//if we made a full loop
      {
      return NULL;  //return null
      }
      index++;    //increment index by 1
      if(index==TABLE_SIZE+1)   //if we are at the end of the table
      {
        index=0;    //go back to begging of table
      }
      trav = tables[index]; //node is equal to new index
    }//end while
    if(trav==NULL){//if we land on an open spot, it is not there
      return NULL;  //return null
    }
    return trav;    //if we do find our value, return it

    //found
  }//end else

}

void Hash::deleteLP(int index, int key){    //lookup the initial index
//if the initial index contains our key, delete the key and set index equal to -1
//if the index does not have our key
Node* curr = searchLP(index, key);    //search to see if our value is in the table
  if(curr==NULL)  //if we dont find our value
  {
    //not in the list
  }
  else    //if it is in the list
  {
  Node* temp = curr;    //set temp value
  delete curr;          //delete our value in node
  temp = NULL;          //set index back to null
  }
}

void Hash::insertCH(int index1, int index2, int key){   //lookup 2 index first
  //insert at first index if empty
  //if first index is full, look for second index
  //if second index is full, insert into second location and move current item to its other location
  //continue loop until the new alternative spot is empty
  Node* ser1 = searchCH(index1, index2, key);   //look for our value in the list
  if(ser1!=NULL)  //if we find it
  {
    //duplicate
  }
  else      //if it isnt in the list
  {
      Node* first = tables[index1];       //pointer to first possible index
      Node* second = tables1[index2];     //pointer to second possible index


      if(first==NULL)
      {
        first->key = key;     //if first spot is open, insert
      }
      else if(second==NULL)
      {
        second->key = key;    //if second spot is open, insert
      }
      else if(first!=NULL && second!=NULL)      //if both of our spots are taken, we have to shift values
      {
          //get node that is currently in our spot
          //replace that node with our value
          //node that was there, find its alternative spot
          //if that spot is also taken repeat the steps above until there is an open spot


        int otherKey = second->key;  //find the key of second spot
        second->key = key;          //put key in its alternative spot
        int nextIndex = Hash1(otherKey);  //find the index for new alternative
        Node* alt = tables[nextIndex];  //point to alt spot in first table
        if(alt==NULL) //if its empty
        {
          alt->key = otherKey; //
        }
        else
        {
          int othKey = alt->key;
          int nexIndex = Hash2(othKey);
        }



      }//end else if
      //if we never find an alternative location, we need to rehash the entire table
}//end big else
}//end function

Node* Hash::searchCH(int index1, int index2, int key){    //lookup 2 index first
  Node* curr = tables[index1];  //find first index for our value
  Node* curr1 = tables1[index2];  //find second index for our value

  if(curr->key == key)      //if the first index has our value
  {
    return curr;          //key in first index, return
  }
  else if(curr1->key == key)    //if the second index has our value
  {
    return curr1;       //key in second index, return
  }
  else if(curr->key != key && curr1->key != key)    //if our key is in neither of the positions
  {
    return NULL;        //key is neither in first nor second spot, return null
  }
}



void Hash::deleteCH(int index1, int index2, int key){   //lookup 2 index first
  Node* curr = searchCH(index1, index2, key);//search for our value at either of the two locations
  if(curr==NULL)    //if it return null, it is not in either table
  {
    //not in table
  }
  else    //if we do find our value
  {
    Node* temp = curr;    //temp value at current index
    delete curr;          //delete the node with our value
    temp = NULL;          //set node equal to null
  }
}
