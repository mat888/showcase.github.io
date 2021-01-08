#include <iostream>
using namespace std;

template <class T>
T* init_arr(T t, long unsigned int size){
	
	//The size of the uniform type portion of the array.
	long unsigned int item_length = sizeof(T) * size;
	
	//Entire array is of size item_length +
	//the int in front holding the count of items in the arr
	long unsigned int* address = (long unsigned int*)malloc(sizeof(long unsigned int) + item_length);

	//This is the current size of the array of type T
	//sitting out in front of this address index.
	*address = 0;

	//Move past the initial size element of the arr into
	void* elem_start = address + sizeof(long unsigned int);

	//Returns address where elements of T start
	return (T*)elem_start;
}

template <class T>
long unsigned int len_arr(T* arr) {
	return *((long unsigned int*)arr - sizeof(long unsigned int));
}

template <class T>
void append_arr(T* arr, T item) {
	//Get the current length so it knows how far up the array to travel to assign item to.
	long unsigned int length = len_arr(arr);

	//Increment the length. 
	*((long unsigned int*)arr - sizeof(long unsigned int)) += 1;

	T* next_address = arr + length;
	*next_address = item;
}

template <class T>
T retrieve(T* arr, long unsigned int index) {
	T item = *(arr + index);
	return item;
}

int main(void) {
	string i = "1234";
	string* my_arr = init_arr(i, 10);

	cout << "Arr addres @ " << ((int*)my_arr - sizeof(int)) << endl;


	string aa = "test aa"; string bb = "test bb"; string cc = "test cc";

	cout << "current length: " << len_arr(my_arr) << endl;

	append_arr(my_arr, aa);
	cout << "current length: " << len_arr(my_arr) << endl;

	append_arr(my_arr, bb);
	cout << "current length: " << len_arr(my_arr) << endl;

	append_arr(my_arr, cc);
	cout << "current length: " << len_arr(my_arr) << endl;


	string a = retrieve(my_arr, 0);
	string b = retrieve(my_arr, 1);
	string c = retrieve(my_arr, 2);
    
	cout << a << endl;
    cout << b << endl;
    cout << c << endl;

	return 0;
}
