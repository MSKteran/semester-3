#include <iostream>
#include <cmath>
#include <cstring>
using namespace std;

template<class T>
class foo
{
    int n;
    T *arr;
public:
    foo();
    foo(int n) {this->n = n; arr = new T[n]; memset(arr, 0, n*sizeof(T));}
    foo(foo<T> *f) {n = f->n; arr = new T[n]; memcpy(arr, f->arr, sizeof(T)*n);}
    int getSize() {return n;}
    ~foo() {delete [] arr;}
    void show() {for(int i = 0; i < n; ++i) cout << arr[i] << ' '; cout << "\n";}
    void setter(int, T);
    T getter(int);
    void add(T);
    static foo<T> sum(foo<T>*, foo<T>*);
    static foo<T> difference(foo<T>*, foo<T>*);

    friend ostream& operator<<(ostream& stream, const foo<T> &f)
    {
        for(int i = 0; i < f.n; ++i) {
            stream << f.arr[i] << ' ';
        }
        stream << "\n";
        return stream;
    }

    foo<T>& operator=(const foo<T>& f)
    {
        if(typeid(f.arr[0]) != typeid(this->arr[0])) {
            throw bad_typeid();
        }
        if(&f != this) {
            delete[] arr;
            n=f.n;
            this->arr = new T[f.n];
            memcpy(arr, f.arr, sizeof(T) * f.n);
        }

        for(int i = 0; i < this->n; ++i) {
            cout << this->arr[i] << ' ';
        }
        return *this;
    }
    static double distanceBetweenVectors(foo<T>*, foo<T>*);

};

int main()
{
    foo<int> f1(5);
    foo<int> f2(5);

    f1.setter(0, 5);
    f1.setter(1, 8);
    f1.setter(2, -2);

    f2.setter(0, 2);
    f2.setter(2, -3);
    f2.setter(4, 9);

    foo<int> f3(5);
    f3 = f1;
    cout << "\nf1: " << f1 << "f3: " << f3 << "\n";

    return 0;
}

template<class T>
foo<T> foo<T>::difference(foo<T> *a, foo<T> *b)
{
    if(a->n != b->n) {
        throw length_error("Length error");
    }
    foo<T> res(a);
    for(int i = 0; i < a->n; ++i) {
        res.arr[i] -= b->arr[i];
    }
    return res;
}

template<class T>
foo<T> foo<T>::sum(foo<T> *a, foo<T> *b)
{
    if(a->n != b->n) {
        throw std::length_error("Length error");
    }
    foo<T> res(a);
    for(int i = 0; i < a->n; ++i) {
        res.arr[i] += b->arr[i];
    }
    return res;
}

template<class T>
void foo<T>::add(T element)
{
    if(typeid(element) != typeid(this->arr[0])) {
        throw bad_typeid();
    }
    if(element < -100 || element > 100) {
        throw std::invalid_argument("Value out of range [-100, 100]\n");
    }
    n++;
    T *temp = new T[n];
    memcpy(temp, arr, (n - 1) * sizeof(int));
    temp[n - 1] = element;
    delete [] arr;
    arr = temp;
}

template<class T>
void foo<T>::setter(int index, T element)
{
    if(element < -100 || element > 100) {
        throw std::invalid_argument("Value out of range [-100, 100]\n");
    }
    if(index < 0 || index >= n) {
        throw std::out_of_range("Wrong index\n");
    }
    arr[index] = element;
}

template<class T>
T foo<T>::getter(int index)
{
    if(index < 0 || index >= n) {
        throw std::out_of_range("Wrong index\n");
    }
    return arr[index];
}

template<class T>
double foo<T>::distanceBetweenVectors(foo<T>* a, foo<T>* b)
{
    if(typeid(a->arr[0]) != typeid(int) || typeid(b->arr[0]) != typeid(int))
        throw bad_typeid();
    if(a->n != b->n)
        throw length_error("Length error");
    double res = 0;
    for(int i = 0; i < a->n; ++i)
        res += pow(a->arr[i] - b->arr[i], 2);
    return sqrt(res);
}
