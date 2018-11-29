#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "studentLL.h"
#include "studentRecord.h"

// linked list node type
// DO NOT CHANGE
typedef struct node {
    studentRecordT data;
    struct node    *next;
} NodeT;

// linked list type
typedef struct ListRep {
   NodeT *head;

/* Add more fields if you wish */

} ListRep;

// Time complexity: O(1)
// Explanation: constant time, do not depend on the number of the input
List newLL() {
    // apply memory depend on the size of the type ListRep
    ListRep *L = malloc(sizeof(ListRep));
    assert(L != NULL);

    L -> head = NULL;
    return L;
}

// Time complexity: O(n)
// Explanation: linear time，depend on the number of the input
void dropLL(List listp) {
    if (listp -> head == NULL){
        free(listp);
        return;
    }

    //free all the node in the list besides the list
    NodeT *list;
    NodeT *p;
    NodeT *pNext;
    list = listp -> head;

    p = list;
    while (p -> next != NULL){
        pNext = p -> next;
        free(p);
        p = pNext;
    }
    free(listp);
    return;
}

// Time complexity: O(n)
// Explanation: linear time, depend on the number of the input
void inLL(List listp, int zid) {
    if (listp -> head == NULL){
        printf("No record found.\n");
    }

    int get_or_not = 0;

    NodeT *list;
    NodeT *p;
    list = listp -> head;

    for (p = list; p != NULL; p = p -> next){
        if (zid == p -> data.zID){
            printStudentData(p -> data.zID, p -> data.credits, p -> data.WAM);
            get_or_not = 1;
        }
    }
    if (get_or_not == 0){
        printf("No record found.\n");
    }
}

// Time complexity: O(n)
// Explanation: linear time, depend on the number of the input
void insertLL(List listp, int zid, int cr, float wam) {
    NodeT *pInsert = malloc(sizeof(NodeT));
    assert(pInsert != NULL);

    pInsert -> data.zID = zid;
    pInsert -> data.credits = cr;
    pInsert -> data.WAM = wam;
    pInsert -> next = NULL;

    if (listp -> head == NULL){
        listp -> head = pInsert;
        printf("Student record added.\n");
        return;
    }

    NodeT *list;
    NodeT *p;
    list = listp -> head;

    for (p = list; p != NULL; p = p -> next){
        if (p -> data.zID == zid){
            p -> data.credits = cr;
            p -> data.WAM = wam;
            printf("Student record updated.\n");
            return;
        }
    }

    NodeT *list1;
    NodeT *p1;
    list1 = listp -> head;

    NodeT *last_node;
    last_node = listp -> head;

    if (zid < listp -> head -> data.zID){
        listp -> head = pInsert;
        pInsert -> next = list1;
        printf("Student record added.\n");
        return;
    }

    p1 = list1;
    while (p1 != NULL){
        if (zid < p1 -> data.zID){
            last_node -> next = pInsert;
            pInsert -> next = p1;
            break;
        }
        if (p1 == last_node){
            p1 = p1 -> next;
        }
        else{
            last_node = p1;
            p1 = p1 -> next;
        }
    }
    if (p1 == NULL){
        last_node -> next = pInsert;
    }
    printf("Student record added.\n");
    return;
}

// stage 2 'a' mode
// void insertLL(List listp, int zid, int cr, float wam) {
//     NodeT *pInsert = malloc(sizeof(NodeT));
//     assert(pInsert != NULL);

//     pInsert -> data.zID = zid;
//     pInsert -> data.credits = cr;
//     pInsert -> data.WAM = wam;
//     pInsert -> next = NULL;

//     if (listp -> head == NULL){
//         listp -> head = pInsert;
//         printf("Student record added.\n");
//         return;
//     }

//     NodeT *list;
//     NodeT *p;
//     list = listp -> head;

//     for (p = list; p != NULL; p = p -> next){
//         if (p -> data.zID == zid){
//             p -> data.credits = cr;
//             p -> data.WAM = wam;
//             printf("Student record updated.\n");
//             return;
//         }
//     }

//     NodeT *firstNode;
//     firstNode = listp -> head;
//     listp -> head = pInsert;
//     pInsert -> next = firstNode;
//     printf("Student record added.\n");
//     return;
// }

// Time complexity: O(n)
// Explanation: linear time, depend on the number of the input
void getStatLL(List listp, int *n, float *wam, float *w_wam) {
    int record = 0;
    int credit_sum = 0;
    float wam_sum = 0.0;
    float w_wam_sum = 0.0;

    if (listp -> head == NULL){
        return;
    }

    NodeT *list;
    NodeT *p;
    list = listp -> head;

    for (p = list; p != NULL; p = p -> next){
        record = record + 1;
        wam_sum = wam_sum + p -> data.WAM;
        w_wam_sum = w_wam_sum + (p -> data.WAM) * (p -> data.credits);
        credit_sum = credit_sum + p -> data.credits;
    }

    *n = record;
    *wam = wam_sum / record;
    *w_wam = w_wam_sum / credit_sum;
    return;

}

// Time complexity: O(n)
// Explanation: linear time, depend on the number of the input
void showLL(List listp) {
    if (listp -> head == NULL){
        printf("Link list is empty!");
        return;
    }
    NodeT *list;
    NodeT *p;
    list = listp -> head;

    for (p = list; p != NULL; p = p -> next){
        printStudentData(p -> data.zID, p -> data.credits, p -> data.WAM);
    }

    return;
}
