#include <iostream>
#include <string>
#include <ctime>
using namespace std;

string generateRandomString(int length)
{
    string result = "";
    for (int i = 0; i < length; i++)
    {
        int random = rand() % 36;
        if (random < 10)
            result += (char)(random + 48);
        else
            result += (char)(random + 87);
    }
    return result;
}

int getHashCode(string str)
{
    int hash = 0;
    for (int i = 0; i < str.length(); i++)
    {
        hash = hash * 31 + str[i];
    }
    return hash;
}

int main()
{
    srand(time(NULL));

    double timesByString[4] = { 0, 0, 0, 0 };
    double timesByHash[4] = { 0, 0, 0, 0 };

    int collisionsByString[4] = { 0, 0, 0, 0 };
    int collisionsByHash[4] = { 0, 0, 0, 0 };

    int lengthOfTest = 10;

    for (int i = 0; i < lengthOfTest; i++)
    {
        for (int length = 3; length <= 6; length++)
        {
            int hashCodes[2000];
            string strings[2000];

            for (int i = 0; i < 2000; i++)
            {
                string str = generateRandomString(length);
                hashCodes[i] = getHashCode(str);
                strings[i] = str;
            }

            clock_t start = clock();

            for (int i = 0; i < 2000; i++)
            {
                for (int j = i + 1; j < 2000; j++)
                {
                    if (strings[i] == strings[j])
                        collisionsByString[length - 3]++;
                }
            }
            clock_t end = clock();
            timesByString[length - 3] += (double)(end - start) / CLOCKS_PER_SEC;

            start = clock();
            for (int i = 0; i < 2000; i++)
            {
                for (int j = i + 1; j < 2000; j++)
                {
                    if (hashCodes[i] == hashCodes[j])
                        collisionsByHash[length - 3]++;
                }
            }
            end = clock();
            timesByHash[length - 3] += (double)(end - start) / CLOCKS_PER_SEC;
        }
    }

    for (int i = 0; i < 4; i++)
    {
        timesByString[i] /= lengthOfTest;
        timesByHash[i] /= lengthOfTest;
        collisionsByString[i] /= lengthOfTest;
        collisionsByHash[i] /= lengthOfTest;
    }

    cout << "Average collisions by string: " << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << "Length " << i + 3 << ": " << collisionsByString[i] << endl;
    }
    cout << endl;
    cout << "Average collisions by hash: " << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << "Length " << i + 3 << ": " << collisionsByHash[i] << endl;
    }
    cout << endl;
    cout << "Average time by string: " << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << "Length " << i + 3 << ": " << timesByString[i] << endl;
    }
    cout << endl;
    cout << "Average time by hash: " << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << "Length " << i + 3 << ": " << timesByHash[i] << endl;
    }
    cout << endl;

    return 0;
}
