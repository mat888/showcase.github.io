#Type flexible array from scratch in C++

```cpp
#include <iostream>
using namespace std;

template <class T>
T* init_arr(T t, int length){
	//Function initializes an array with the current size
	//as an integer at its memory address, and then a true
	//single type array following that.
	
	//The length of the uniform type portion of the array.
	int item_length = sizeof(T) * length;
	
	//Entire array is of size item length plus 'current size'
	//element which sits at the front.
	int* address = (int*)malloc(sizeof(int) + item_length);

	//This is the current size of the sub array of type T
	//sitting out in front of this address index.
	*address = 0;

	//Move past the initial size element of the arr into
	//the sub-arr of uniform type that comes after.
	void* elem_start = address + sizeof(int);
	//Returns address where elements start, not the hidden first
	//element of 'size.'
	return (T*)elem_start;
}

template <class T>
void append_arr(T* arr, T item){
	//Get the size so it knows how far up the array to travel to assign item to.
	int size = *((int*)arr - sizeof(int));

	//Increment the size. 
	*((int*)arr - sizeof(int)) += 1;

	T* next_addres = arr + size;
	*next_addres = item;
}

template <class T>
T retrieve(T* arr, int index) {
	T item = *(arr + index);
	//cout << "Item at index, " << index << ": " <<item << endl;
	return item;
}

int main(void) {
	string i = "1234";
	string* my_arr = init_arr(i, 10);

	string aa = "test0"; 
	string bb = "test1";
	string cc = "test2";

	append_arr(my_arr, aa);
	append_arr(my_arr, bb);
	append_arr(my_arr, cc);

	string a = retrieve(my_arr, 0);
	string b = retrieve(my_arr, 1);
	string c = retrieve(my_arr, 2);

	cout << *((int*)my_arr - sizeof(int)) << endl;
    
	cout << a << endl;
    cout << b << endl;
    cout << c << endl;


	//cout << "end" << endl;
	return 0;
}

```