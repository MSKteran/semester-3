#include <clocale>
#include <iostream>
#include <conio.h>
using namespace std;

template<class T>
struct Node
{
    int id, accessCounter;
    T data;
    Node *next;
    Node(T data_, int id_) : data(data_), id(id_), next(nullptr), accessCounter(0) {}
    friend ostream& operator<<(ostream& stream, const Node<T>& node) {
        stream << "\n\tid: " << node.id << "\n\taccessCounter: " << node.accessCounter;
        stream << "\n\tdata: " << node.data;
        return stream;
    }
};

template<class T>
class CacheList
{
    Node<T> *first;
    int idCounter;
public:
    CacheList() : first(nullptr), idCounter(1) {}
    CacheList(Node<T>* node) : first(node), idCounter(1) {}
    Node<T>* getData(int id);
    void print();
};

int main()
{
    setlocale(0, "");

    //////////  Добавление 5 элементов в список  ///////////
    Node<string> *node1 = new Node<string>("product1", 1);
    Node<string> *node2 = new Node<string>("product2", 2);
    node1->next = node2;
    Node<string> *node3 = new Node<string>("product3", 3);
    node2->next = node3;
    Node<string> *node4 = new Node<string>("product4", 4);
    node3->next = node4;
    Node<string> *node5 = new Node<string>("product5", 5);
    node4->next = node5;
    CacheList<string> cacheList(node1);
    ////////////////////////////////////////////////////////

    cacheList.print();
    char choice;
    while(1) {
        while(2) {
            choice = _getch();
            if(choice >= 49 && choice <= 53)
                break;
            if(choice == 13 || choice == 27) exit(1);
        }
        Node<string>* temp = cacheList.getData(choice - 48);
        system("cls");
        cacheList.print();
    }

    return 0;
}


template<class T>
Node<T>* CacheList<T>::getData(int id)
{
    if(first->id == id) {
        first->accessCounter++;
        return first;
    }
    Node<T>* beforeCurrent = first;
    Node<T>* current = beforeCurrent->next;
    while(current) {
        if(current->id == id) {
            current->accessCounter++;
            beforeCurrent->next = current->next;

            if(current->accessCounter >= first->accessCounter) {
                current->next = first;
                first = current;
                return first;
            }
            beforeCurrent = first;
            while(beforeCurrent->next && beforeCurrent->next->accessCounter > current->accessCounter) {
                beforeCurrent = beforeCurrent->next;
            }
            current->next = beforeCurrent->next;
            beforeCurrent->next = current;
            return current;
        }
        beforeCurrent = current;
        current = current->next;
    }
}

template<class T>
void CacheList<T>::print()
{
    Node<T>* current = first;
    while(current) {
        cout << *current << "\n";
        current = current->next;
    }
}
