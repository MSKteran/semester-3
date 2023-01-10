#include <iostream>
#include <map>
#include <string>
#include <algorithm>
#include <vector>
#include <sstream>
#include <time.h>
using namespace std;

void func_map()
{
    map<string, int> counts;

    string input;
    getline(cin, input);
    input += " ";

    string word;
    for (auto &c : input)
    {
        if (c == ' ')
        {
            ++counts[word];
            word.clear();
        }
        else
            word += c;
    }

    for (const auto &words : counts)
        cout << words.first << ": " << words.second << endl;
}

void func_vector()
{
    srand(time(NULL));
    int size1, size2;
    cin >> size1 >> size2;

    vector<int> vec1(size1), vec2(size2);
    generate(vec1.begin(), vec1.end(), []() { return rand() % 201 - 100; });
    generate(vec2.begin(), vec2.end(), []() { return rand() % 201 - 100; });


    for (const auto &x : vec1)
        cout << x << ' ';
    cout << '\n';

    for (const auto &x : vec2)
        cout << x << ' ';
    cout << '\n';

    double mean1 = 0, mean2 = 0;
    for (const auto &x : vec1)
        mean1 += x;
    mean1 /= vec1.size();

    for (const auto &x : vec2)
        mean2 += x;
    mean2 /= vec2.size();

    cout << mean1 << '\n';
    cout << mean2 << '\n';

    vector<int> intersect;
    set_intersection(vec1.begin(), vec1.end(), vec2.begin(), vec2.end(), back_inserter(intersect));

    for (const auto &x : intersect)
        cout << ' ' << x;
}

bool isPassed(vector<int>& visitRecord)
{
    for(auto x : visitRecord)
        if(x == 1) return 0;
    return 1;
}

void func_stack()
{
    int n;
    cin >> n;
    vector<vector<int>> v(n);
    int a;
    string input;
    for(int i = 0; i < n; ++i) {
        cin.sync();
        getline(cin, input);

        while(find(input.begin(), input.end(), ' ') != input.end()) {
            a = atoi(input.substr(0, input.find(' ')).c_str());
            v[i].push_back(a - 1);
            input.erase(0, input.find(' ') + 1);
        }

        a = atoi(input.c_str());
        v[i].push_back(a - 1);
    }

    vector<vector<bool>> res(n, vector<bool>(n));
    for(int i = 0; i < n; ++i)
        res[i][i] = 1;

    for(int i = 0; i < n; ++i) {
        vector<int> visitRecord(n);
        for(auto x : v[i]) {
            if(x=-1) break;
            visitRecord[x] = 1;
        }
        while(!isPassed(visitRecord)) {
            for(int j = 0; j < n; ++j) {
                if(visitRecord[j] == 1) {
                    res[i][j] = 1;
                    for(auto x : v[j])
                        if(x=-1) break;
                        else if(visitRecord[x] != 2) visitRecord[x] = 1;
                    visitRecord[j] = 2;
                }
            }
        }
    }

    for(int i = 0; i < n; ++i) {
        cout << '\n';
        for(int j = 0; j < n; ++j)
            cout << res[i][j] << "  ";
    }
}

int main()
{
    func_map();
    cout << "\n";
    func_vector();
    cout << "\n";
    func_stack();
    cout << "\n";
    return 0;
}
