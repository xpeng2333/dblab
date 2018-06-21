#include <cstdio>
#include <cstring>
#include <iostream>
#include <sstream>
#include <vector>

#define FREE 0
#define SLOCK 1
#define XLOCK 2
#define UPDATELOCK 3

typedef struct lockInfo {
    int transactionID;
    char object;
    int lockType;
} lockInfo;

using namespace std;

int i, j;
int lockTable[26][256] = {0};
int count[256] = {0};
bool compatibilityMatrix[4][4] = {
    {1, 1, 1, 0}, {1, 1, 0, 1}, {1, 0, 0, 0}, {1, 0, 0, 0}};
string lockTypeMap[4] = {"Free", "S-lock", "X-lock", "Update-lock"};
vector<lockInfo> lockBuff;
vector<lockInfo>::iterator it;

void tryGrant() {
    int tmpTransactionID;
    char tmpObject;
    int tmpLockType;
    while (1) {
        if (lockBuff.size() == 0)
            break;
        tmpTransactionID = (lockBuff.at(0)).transactionID;
        tmpObject = (lockBuff.at(0)).object;
        tmpLockType = (lockBuff.at(0)).lockType;
        for (i = 0; i < 256; i++) {
            if (i == tmpTransactionID) {
                continue;
            }
            if (!compatibilityMatrix[lockTable[tmpObject - 'A'][i]]
                                    [tmpLockType]) {
                break;
            }
        }
        if (i == 256) {
            lockTable[tmpObject - 'A'][tmpTransactionID] = tmpLockType;
            lockBuff.erase(lockBuff.begin());
            count[tmpTransactionID]--;
            cout << lockTypeMap[tmpLockType] << " on " << tmpObject
                 << " granted to " << tmpTransactionID << endl;
        } else if (tmpLockType == 2) {
            for (j = i; j < 256; j++) {
                if (lockTable[tmpObject - 'A'][j] == 2 ||
                    lockTable[tmpObject - 'A'][j] == 3) {
                    break;
                }
            }
            if (j == 256) {
                lockTable[tmpObject - 'A'][tmpTransactionID] = 3;
                lockBuff.erase(lockBuff.begin());
                count[tmpTransactionID]--;
                cout << lockTypeMap[3] << " on " << tmpObject << " granted to "
                     << tmpTransactionID << endl;
            }
        } else {
            break;
        }
    }
}

int main(int argc, char const *argv[]) {
    for (i = 0; i < 26; i++) {
        for (j = 0; j < 256; j++) {
            lockTable[i][j] = 0;
        }
    }
    for (i = 0; i < 256; i++) {
        count[i] = 0;
    }
    string tmp;
    string requestType;
    int transactionID;
    char object;
    lockInfo tmpLock;
    while (1) {
        cout << "> ";
        getline(cin, tmp);
        stringstream command(tmp);
        command >> requestType;
        command >> transactionID;
        if (requestType == "Start") {
            cout << "Start " << transactionID << " : Transaction "
                 << transactionID << " started" << endl;
        } else if (requestType == "End") {
            cout << "End " << transactionID << " : Transaction ended" << endl;
            for (int i = 0; i < 26; i++) {
                if (lockTable[i][transactionID]) {
                    cout << "Release "
                         << lockTypeMap[lockTable[i][transactionID]] << " on "
                         << (char)('A' + i) << endl;
                    lockTable[i][transactionID] = 0;
                    int tmpcount = 0;
                    for (j = 0; j < 256; j++) {
                        if (lockTable[i][j] == 1)
                            tmpcount++;
                    }
                    if (!tmpcount) {
                        for (j = 0; j < 256; j++) {
                            if (lockTable[i][j] == 3) {
                                lockTable[i][j] = 2;
                                cout << "XLock " << j << " " << char(i + 'A')
                                     << ": Upgrade to X-lock granted" << endl;
                                break;
                            }
                        }
                    }
                }
            }
            for (it = lockBuff.begin(); it != lockBuff.end();) {
                if ((*it).transactionID == transactionID) {
                    it = lockBuff.erase(it);
                } else {
                    it++;
                }
            }
            count[transactionID] = 0;
            if (!lockBuff.empty()) {
                tryGrant();
            }
        } else if (requestType == "SLock") {
            command >> object;
            tmpLock.lockType = 1;
            tmpLock.object = object;
            tmpLock.transactionID = transactionID;
            if (count[transactionID]) {
                lockBuff.push_back(tmpLock);
                count[transactionID]++;
                cout << "SLock " << transactionID << " " << object
                     << ": the current transaction is waiting!" << endl;

            } else {
                for (i = 0; i < 256; i++) {
                    if (!compatibilityMatrix[lockTable[object - 'A'][i]][1])
                        break;
                }
                if (i == 256) {
                    lockTable[object - 'A'][transactionID] = 1;
                    cout << "SLock " << transactionID << " " << object
                         << ": Lock granted" << endl;
                } else {
                    lockBuff.push_back(tmpLock);
                    count[transactionID]++;
                    cout << "SLock " << transactionID << " " << object
                         << ": Waiting for lock (X-lock held by: " << i << " )"
                         << endl;
                }
            }
        } else if (requestType == "XLock") {
            command >> object;
            tmpLock.lockType = 2;
            tmpLock.object = object;
            tmpLock.transactionID = transactionID;
            if (count[transactionID]) {
                lockBuff.push_back(tmpLock);
                count[transactionID]++;
                cout << "XLock " << transactionID << " " << object
                     << ": the current transaction is waiting!" << endl;

            } else {
                for (i = 0; i < 256; i++) {
                    if (!compatibilityMatrix[lockTable[object - 'A'][i]][2])
                        break;
                }
                if (i == 256) {
                    lockTable[object - 'A'][transactionID] = 2;
                    cout << "XLock " << transactionID << " " << object
                         << ": Lock granted" << endl;
                } else {
                    if (lockTable[object - 'A'][i] == 1) {
                        cout << "XLock " << transactionID << " " << object
                             << ": Waiting for lock (S-lock held by: ";
                        for (j = i; j < 256; j++) {
                            if (lockTable[object - 'A'][j] == 1) {
                                cout << j << " ";
                            }
                        }
                        cout << ")" << endl;
                        while (i < 256) {
                            if (!compatibilityMatrix[lockTable[object - 'A'][i]]
                                                    [2])
                                if (lockTable[object - 'A'][i] != 1)
                                    break;
                            i++;
                        }
                        if (i == 256)
                            lockTable[object - 'A'][transactionID] = 3;
                        else {
                            lockBuff.push_back(tmpLock);
                            count[transactionID]++;
                        }

                    } else {
                        lockBuff.push_back(tmpLock);
                        count[transactionID]++;
                        cout << "XLock " << transactionID << " " << object
                             << ": Waiting for lock ("
                             << lockTypeMap[lockTable[object - 'A'][i]]
                             << " held by: " << i << " )" << endl;
                    }
                }
            }

        } else if (requestType == "Unlock") {
            lockTable[object - 'A'][transactionID] = 0;
            cout << "Unlock " << transactionID << " " << object
                 << " : Lock released" << endl;
            int tmpcount = 0;
            for (i = 0; i < 256; i++) {
                if (lockTable[object - 'A'][i] == 1)
                    tmpcount++;
            }
            if (!tmpcount) {
                for (i = 0; i < 256; i++) {
                    if (lockTable[object - 'A'][i] == 3) {
                        lockTable[object - 'A'][i] = 2;
                        cout << "XLock " << i << " " << object
                             << ": Upgrade to X-lock granted" << endl;
                        break;
                    }
                }
            }
            if (!lockBuff.empty()) {
                tryGrant();
            }
        } else if (requestType == "Show") {
            for (i = 0; i < 26; i++) {
                for (j = 0; j < 256; j++) {
                    if (lockTable[i][j]) {
                        cout << (char)('A' + i) << " is locking by "
                             << lockTypeMap[lockTable[i][j]] << " " << j
                             << endl;
                    }
                }
            }
            for (it = lockBuff.begin(); it != lockBuff.end(); it++) {
                cout << (*it).transactionID << " "
                     << lockTypeMap[(*it).lockType] << " is waiting to lock "
                     << (*it).object << endl;
            }
        } else {
            cout << "命令错误!" << endl;
        }
    }
    return 0;
}
