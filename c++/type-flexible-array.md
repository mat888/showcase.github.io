## Type/length flexible array from scratch in C++

Building from scratch array functionality in C++ to familiarize oneself intamately with the data structure and practice clean code.

The best parts of this function set are the simple and intuitive user end functions, which are internally light, easy to read, and general.
Room for improvement could come in the way of a more universal length function (see below) and the inclusion of a wider set of features like editing or deleting specific indices.

The array is initiliazed with an `int` at its start address, but returns the address past that `int` cast as a pointer to the desired type, with memory allocated for that type and the given size. This keeps the `length` address *behind* the array but accessible to functions on arrays.

The first element is an `int` which tracks the current length and can be set at creation

```cpp
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
```
The length of the array is given by `*((long unsigned int*)arr - sizeof(long unsigned int))`, the address given by `init_arr` minus the size of its hidden first element.

```cpp
template <class T>
long unsigned int len_arr(T* arr) {
	return *((long unsigned int*)arr - sizeof(long unsigned int));
}
```
`append_arr` uses the `len_arr` function above to get the legnth and determine how far down the array to append the given item. It would have been nice to have a solution that reused the function to also increment the length value in the array itself, rather than reusing the same line of code.

```cpp
template <class T>
void append_arr(T* arr, T item) {
	long unsigned int length = len_arr(arr);

	//Increment the length value in the array.
	*((long unsigned int*)arr - sizeof(long unsigned int)) += 1;

	T* next_address = arr + length;
	*next_address = item;
}
```
Since the array's return  address starts past the hidden `length` index, this function is straightforward:
```cpp
template <class T>
T retrieve(T* arr, long unsigned int index) {
	T item = *(arr + index);
	return item;
}
```
The basic testing:
```cpp
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
```
