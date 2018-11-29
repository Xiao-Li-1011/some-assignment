/**
     main.c

     Program supplied as a starting point for
     Assignment 1: Student record manager

     COMP9024 17s2
**/
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <ctype.h>

#include "studentRecord.h"
#include "studentLL.h"

void printHelp();
void StudentLinkedListProcessing();

int main(int argc, char *argv[]) {
   if (argc == 2) {

      // get the number of record which should be input
      int numberOfStudent;
      sscanf(argv[1], "%d", &numberOfStudent);

      // apply the memory depend on the number of student record
      studentRecordT *students = malloc(numberOfStudent * sizeof(studentRecordT));
      assert(students != NULL);

      int id, credit, totalCredit;
      float WAM, averageWAM, weightedAverageWAM, totalWAM, totalWeightedWAM;

      id = -1;
      credit = -1;
      WAM = -1;
      totalCredit = 0;
      averageWAM = 0.0;
      weightedAverageWAM = 0.0;
      totalWAM = 0.0;
      totalWeightedWAM = 0.0;

      // loop for get valid ids, credits and WAMs
      for (int student = 0; student < numberOfStudent; student++){
         printf("Enter student ID: ");
         id = readValidID();
         // to compute if the id is exist
         for (int i = 0; i < student; i++){
            if (id == students[i].zID)
               id = -1;
         }
         while (id == -1){
               printf("Not valid. Enter a valid value: ");
               id = readValidID();
               for (int i = 0; i < student; i++){
                  if (id == students[i].zID)
                     id = -1;
               }
         }
      
         printf("Enter credit points: ");
         credit = readValidCredits();
         while (credit == -1){
                printf("Not valid. Enter a valid value: ");
                credit = readValidCredits();
         }

         printf("Enter WAM: ");
         WAM = readValidWAM();
         while (WAM == -1){
                printf("Not valid. Enter a valid value: ");
                WAM = readValidWAM();
         }

         students[student].zID = id;
         students[student].credits = credit;
         students[student].WAM = WAM;

         totalCredit = totalCredit + credit;
         totalWAM = totalWAM + WAM;
         totalWeightedWAM = totalWeightedWAM + WAM * credit;
      }

      // loop for print records
      for (int student = 0; student < numberOfStudent; student++){
         printStudentData(students[student].zID, students[student].credits, students[student].WAM);
      }

      printf("Average WAM: %.3f\n", totalWAM / numberOfStudent);
      printf("Weighted average WAM: %.3f\n", totalWeightedWAM / totalCredit);
      free(students);

   } else {
      StudentLinkedListProcessing();
   }
   return 0;
}

void StudentLinkedListProcessing() {
   int op, ch;

   List list = newLL();   // create a new linked list
   
   while (1) {
      printf("Enter command (a,f,g,p,q, h for Help)> ");

      do {
	     ch = getchar();
      } while (!isalpha(ch) && ch != '\n');  // isalpha() defined in ctype.h
    op = ch;
      // skip the rest of the line until newline is encountered
      while (ch != '\n') {
	 ch = getchar();
      }

   int id, credit;
   float WAM;

   id = -1;
   credit = -1;
   WAM = -1; 

   int n = 0;
   float wam = 0;
   float w_wam = 0;

      switch (op) {

         case 'a':
         case 'A':

            printf("Enter student ID: ");
            id = readValidID();
            while (id == -1){
                  printf("Not valid. Enter a valid value: ");
                  id = readValidID();
               }
      
            printf("Enter credit points: ");
            credit = readValidCredits();
            while (credit == -1){
                   printf("Not valid. Enter a valid value: ");
                   credit = readValidCredits();
            }

            printf("Enter WAM: ");
            WAM = readValidWAM();
            while (WAM == -1){
                   printf("Not valid. Enter a valid value: ");
                   WAM = readValidWAM();
            }
            insertLL(list, id, credit, WAM);

	    break;

         case 'f':
         case 'F':
            printf("Enter student ID: ");
            id = readValidID();
            while (id == -1){
                  printf("Not valid. Enter a valid value: ");
                  id = readValidID();
               }
            inLL(list, id);

	    break;
	    
         case 'g':
         case 'G':

            getStatLL(list, &n, &wam, &w_wam);
            printf("Number of records: %d\n", n);
            printf("Average WAM: %.3f\n", wam);
            printf("Average weighted WAM: %.3f\n", w_wam);

	    break;
	    
         case 'h':
         case 'H':
            printHelp();
	    break;
	    
         case 'p':
         case 'P':

            showLL(list);

	    break;

	 case 'q':
         case 'Q':
            dropLL(list);       // destroy linked list before returning
	    printf("Bye.\n");
	    return;
      }
   }
}

void printHelp() {
   printf("\n");
   printf(" A - Add student record\n" );
   printf(" F - Find student record\n" );
   printf(" G - Get statistics\n" );
   printf(" H - Help\n");
   printf(" P - Print all records\n" );
   printf(" Q - Quit\n");
   printf("\n");
}
