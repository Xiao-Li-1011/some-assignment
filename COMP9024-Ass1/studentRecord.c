// Student record implementation ... Assignment 1 COMP9024 17s2
#include <stdio.h>

#define LINE_LENGTH 1024

// scan input for a positive integer, returns -1 if none
int readInt(void) {
   char line[LINE_LENGTH];
   int  n;

   fgets(line, LINE_LENGTH, stdin);
   if ( (sscanf(line, "%d", &n) != 1) || n <= 0 )
      return -1;
   else
      return n;
}

// scan input for a positive floating point number, returns -1 if none
float readFloat(void) {
   char  line[LINE_LENGTH];
   float f;

   fgets(line, LINE_LENGTH, stdin);
   if ( (sscanf(line, "%f", &f) != 1) || f <= 0.0 )
      return -1;
   else
      return f;
}

//scan input for a valid id which should be a 7-digit number, returns -1 if none, returns id if valid
int readValidID(void) {
   int id, count;
   count = 0;
   id = readInt();

   if (id == -1)
      return -1;

   int n = id;

   while (n != 0){
      n = n / 10;
      count++;
   }
   if (count != 7)
      return -1;
   else
      return id;  
}

//scan input for a valid credit which should be 2 ~ 480, returns -1 if done, returns credit if valid 
int readValidCredits(void) {
   int credit;
   credit = readInt();

   if (credit == -1)
      return -1;

   if (credit >= 2 && credit <= 480)
      return credit;
   else
      return -1;
}

//scan input for a valid WAM which should be 50.0 ~ 100.0, returns -1 if done, returns WAM if valid 
float readValidWAM(void) {
   float WAM;
   WAM = readFloat();

   if (WAM == -1)
      return -1;

   if (WAM >= 50.0 && WAM <= 100.0)
      return WAM;
   else
      return -1;
}

void printStudentData(int zID, int credits, float WAM) {
   printf("------------------------\n");
   printf("Student zID: z%d\n", zID);
   printf("Credits: %d\n", credits);
   if (WAM >= 85.0 && WAM <= 100.0)
      printf("Level of performance: HD\n");
   else if (WAM >= 75.0 && WAM < 85.0)
      printf("Level of performance: DN\n");
   else if (WAM >= 65.0 && WAM < 75.0)
      printf("Level of performance: CR\n");
   else if (WAM >= 50.0 && WAM < 65.0)
      printf("Level of performance: PS\n");
   printf("------------------------\n");
   return;
}
