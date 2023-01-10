#include <iostream>
#include <fstream>
#include <vector>
#include <typeinfo>
#include <string>
using namespace std;

struct Object
{
    int proportion;
    int price;
    int amount;
    string color;
};

vector<Object> readFromFile()
{
    ifstream fin("objects.txt");
    vector<Object> objs;

    while(true)
    {
        Object obj;
        fin >> obj.proportion >> obj.price >> obj.amount >> obj.color;
        if (!fin)
            break;
        objs.push_back(obj);
    }
    fin.close();
    return objs;
}

vector<Object> searchFromFile(const vector<Object>& objs, const string& param, const string& param_type, const string& value)
{
    vector<Object> res;

    for(const Object& obj : objs)
    {
        if(param == "proportion")
        {
            if(param_type == ">")
            {
                if(obj.proportion > stof(value))
                    res.push_back(obj);
            }
            else if(param_type == "<")
            {
                if(obj.proportion < stof(value))
                    res.push_back(obj);
            }
            else if(param_type == "==")
            {
                if(obj.proportion == stof(value))
                    res.push_back(obj);
            }
        }
        else if(param == "price")
        {
            if(param_type == ">")
            {
                if(obj.price > stof(value))
                    res.push_back(obj);
            }
            else if(param_type == "<")
            {
                if(obj.price < stof(value))
                    res.push_back(obj);
            }
            else if(param_type == "==")
            {
                if(obj.price == stof(value))
                    res.push_back(obj);
            }
        }
        else if(param == "amount")
        {
            if(param_type == ">")
            {
                if(obj.amount > stof(value))
                    res.push_back(obj);
            }
            else if(param_type == "<")
            {
                if(obj.amount < stof(value))
                    res.push_back(obj);
            }
            else if(param_type == "==")
            {
                if(obj.amount == stof(value))
                    res.push_back(obj);
            }
        }
        else if(param == "color")
        {
            if(obj.color == value)
                res.push_back(obj);
        }
    }
    return res;
}

int main()
{
    setlocale(LC_ALL, "russian");
    vector<Object> objs = readFromFile();

    while(true)
    {
        string param;
        string value;
        cout << "�������� ��������: proportion, price, amount, color.\n��� ������ ���� ���������� ������� all.\n��� ������ ������� reset" << endl;
        cin >> param;

        if(param == "all")
        {
            for(const Object& obj : objs)
                cout << obj.proportion << " " << obj.price << " " << obj.amount << " " << obj.color << endl;
            cout << "������� ��������: " << objs.size() << endl;
            cout << endl;
            continue;
        }
        else if(param == "reset")
        {
            objs = readFromFile();
            cout << endl;
            continue;
        }

        cout << "������� ��������: ";
        string param_type;
        cin >> param_type;

        cout << "������� ��������: ";
        cin >> value;

        vector<Object> res = searchFromFile(objs, param, param_type, value);

        if(!res.empty())
        {
            for(const Object& obj : res)
                cout << obj.proportion << " " << obj.price << " " << obj.amount << " " << obj.color << endl;
        }
        cout << "������� ��������: " << res.size() << endl;
        cout << endl;

        objs = res;
    }
    return 0;
}
