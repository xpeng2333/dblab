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
string lockTypeMap[4] = {"Free", "S-lock", "X-lock", "Update"};
vector<lockInfo> lockBuff;
vector<lockInfo>::iterator it;

void tryGrant() {
    int tmpTransactionID;
    char tmpObject;
    int tmpLockType;
    while (1) {
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
            printf("%s on %c granted to %d\n", lockTypeMap[tmpLockType],
                   tmpObject, tmpTransactionID);
        } else {
            break;
        }
    }
}

int main(int argc, char const *argv[]) {
    string tmp;
    string requestType;
    int transactionID;
    char object;
    lockInfo tmpLock;
    // printf("fheg%s\n", lockTypeMap[2]);
    // cout << lockTypeMap[2] << endl;
    while (1) {
        getline(cin, tmp);
        stringstream command(tmp);
        command >> requestType;
        command >> transactionID;
        if (requestType == "Start") {
            printf("Start %d : Transaction %d started\n", transactionID,
                   transactionID);
        } else if (requestType == "End") {
            printf("End %d : Transaction ended\n", transactionID);
            for (int i = 0; i < 26; i++) {
                if (lockTable[i][transactionID])
                    printf("Release %s on %c\n",
                           lockTypeMap[lockTable[i][transactionID]], 'A' + i);
                lockTable[i][transactionID] = 0;
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
                printf("SLock %d %c: the current transaction is waiting!\n",
                       transactionID, object);

            } else {
                for (i = 0; i < 256; i++) {
                    if (!compatibilityMatrix[lockTable[object - 'A'][i]][1])
                        break;
                }
                if (i == 256) {
                    lockTable[object - 'A'][transactionID] = 1;
                    printf("SLock %d %c: Lock granted\n", transactionID,
                           object);
                } else {
                    lockBuff.push_back(tmpLock);
                    count[transactionID]++;
                    printf(
                        "SLock %d %c: Waiting for lock (X-lock held by: %d )\n",
                        transactionID, object, i);
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
                printf("SLock %d %c: the current transaction is waiting!\n",
                       transactionID, object);

            } else {
                for (i = 0; i < 256; i++) {
                    if (!compatibilityMatrix[lockTable[object - 'A'][i]][1])
                        break;
                }
                if (i == 256) {
                    lockTable[object - 'A'][transactionID] = 2;
                    printf("XLock %d %c: Lock granted\n", transactionID,
                           object);
                } else {
                    if (lockTable[object - 'A'][i] == 1) {
                        lockTable[object - 'A'][transactionID] = 3;
                        printf("XLock %d %c: Waiting for lock (S-lock held by: "
                               "%d )\n",
                               transactionID, object, i);
                    } else {
                        lockBuff.push_back(tmpLock);
                        count[transactionID]++;
                        printf("XLock %d %c: Waiting for lock (X-lock held by: "
                               "%d )\n",
                               transactionID, object, i);
                    }
                }
            }

        } else if (requestType == "Unlock") {
            lockTable[object - 'A'][transactionID] = 0;
            count[transactionID]--;
            printf("Unlock %d %c : Lock released\n", transactionID, object);
            for (i = 0; i < 256; i++) {
                if (lockTable[object - 'A'][i] == 3) {
                    lockTable[object - 'A'][i] = 2;
                    printf("XLock %d %c: Upgrade to X-lock granted\n", i,
                           object);
                }
            }
            if (!lockBuff.empty()) {
                tryGrant();
            }
        } else {
            cout << "命令错误!" << endl;
        }
    }
    return 0;
}
