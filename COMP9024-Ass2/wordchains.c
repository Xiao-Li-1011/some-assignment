/*
    Task 1 : compute and output, for each word ω, all words that could immediately follow ω in a word chain,
        depending on the number n of words and the maximum length m of a word.

        n words shold be compare 0 + 1 + 2 + ... + n - 1 times, then the complexity is O(n^2)
        in function CompareWord, the worst case should be compare two longest words, then the complexity is O(m)

        Thus, task 1 : complexity is O(n^2 + m)

    Task 2 : compute and output,
        depending on the number n of words.
        a. the maximum length of a word chain that can be built from the given words,

            Dijkstra’s algorithm to find the maximum length, then complexity is O(n)

        b. all word chains of maximum length that can be built from the given words.

            DFS to find all word chains of maximum length, then complexity is O(n^3)
            In addition, because using Dijkstra’s algorithm to simply the graph, the complexity actually is 
            lower than O(n^3)
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

#include "stack.h"

#define LINE_LENGTH 1024
#define MAX_WORD_LENGTH 20
#define WORD_FORMAT "%19s"

int CompareWord(char*, char*);
// function to compare two words if changed one letter return 1 else return 0 

int main(){

    int n; // the number of the words
    int i, j, k;
    char line[LINE_LENGTH];

    // 1. Input the word number(n >= 1)

    printf("Enter a number: ");
    fgets(line, LINE_LENGTH, stdin);
    if ((sscanf(line, "%d", &n) != 1) || n <= 0){
        printf("Incorrect Input! \n");
        exit(0);
    }
    
    int graph[n][n];
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            graph[i][j] = 0;
    // initialization of the graph which be saved as adjacency matrix  

    char words[n][MAX_WORD_LENGTH]; // save input words
    int inWord, Word;

    // 2. Input the words in alphabetical order

    for (inWord = 0; inWord < n; inWord++){
        printf("Enter word: ");
        scanf(WORD_FORMAT, words[inWord]);
        //no word has more than 19 characters

        for (Word = 0; Word < inWord; Word++){
            if (CompareWord(words[inWord], words[Word])){
                graph[Word][inWord] = 1;
                // only one edge should be added because the graph is a directed graph
            }
        }
    }
    printf("\n");
    
    // 3. Show all the words could immediately follow each word in the word chains

    for (i = 0; i < n; i++){
        printf("%s: ", words[i]);
        for (j = 0; j < n; j++){
            if (graph[i][j]){
                printf("%s ", words[j]);
            }  
        }
        printf("\n");
    }
    printf("\n");

    // 4. Get the Max length and all the word chains which has the Max length 

    // Using Dijkstra’s algorithm to get the longest length and simply the graph
    // Example : 1 -> 2, 1 -> 4, 2 -> 4, then delete the edges 1 -> 4. 

    // the length array initialization
    int distance[n];
    for (i = 0; i < n; i ++){
        distance[i] = 0;
    }

    // record last node 
    // Example : 1 -> 2, 1 -> 3, 2 -> 4, 3 -> 4, then the node 4 last node should be 2, 3.
    int last[n][n];
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            last[i][j] = -1;

    for (i = 0; i < n; i ++){
        for (j = 0; j < n; j++){
            if (graph[i][j]){
                int lastLength = distance[i];
                if (lastLength + 1 == distance[j]){
                    int k = 0;
                    while (last[j][k] != -1){
                        k++;
                    }
                    last[j][k] = i;
                }
                else if (lastLength + 1 > distance[j]){
                    distance[j] = lastLength + 1;
                    for (k = 0; k < n; k ++){
                        last[j][k] = -1;
                    }
                    last[j][0] = i;
                }
            }
        }
    }

    // Get the longest length  
    int longestLength = 0;
    for (i = 0; i < n; i++){
        if (distance[i] > longestLength){
            longestLength = distance[i];
        }
    }
    longestLength++;

    // Get the simple graph
    int simpleGraph[n][n];

    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            simpleGraph[i][j] = 0;

    for (i = 0; i < n; i++){
        for (j = 0; j < n; j++){
            if (last[i][j] != -1){
                simpleGraph[last[i][j]][i] = 1;
            }
        }
    }

    printf("Maximum chain length: %d\n", longestLength);
    printf("Maximal chains:\n");

    // Using deep-first search to get the maximal chains. 
    int dfsLast[n];
    stack s = newStack(); // for dfs algorithm
    stack sOutput = newStack(); // support output
    int end = 1; // determine if the node is the end of a chains
    int computeNode; 
    int count = 0; 

    // dfs
    for (i = 0; i < n; i++){
        for (j = 0; j < n; j++){
            dfsLast[j] = -1;
        }

        StackPush(s, i);

        while (StackIsEmpty(s) == 0){

            computeNode = StackPop(s);

            for (j = n - 1; j > computeNode - 1; j--){
                if (simpleGraph[computeNode][j]){
                    end = 0;
                    StackPush(s, j);
                    dfsLast[j] = computeNode;
                }
            }

            if (end == 1){
                int node = computeNode;
                while (node != i){
                    StackPush(sOutput, node);
                    node = dfsLast[node];
                    count++;
                }
                StackPush(sOutput, i);
                count++;

                if (count == longestLength){
                    while (StackIsEmpty(sOutput) == 0){
                        int nodeOut = StackPop(sOutput);
                        count--; 
                        if (count == 0){
                            printf("%s\n", words[nodeOut]);
                        }
                        else{
                            printf("%s -> ", words[nodeOut]);
                        }
                    }
                }
                else{
                    while (StackIsEmpty(sOutput) == 0){
                        StackPop(sOutput);
                    }
                }
            }

            end = 1;
            count = 0;
        }
    }

    return 0;
}


// support function for comparing two words
int CompareWord(char *word1, char *word2){
    int i;

    if (strlen(word1) == strlen(word2)){

        int diff = 0;

        for (i = 0; i < strlen(word1); i++){
            if (*(word1 + i) != *(word2 + i))
                diff++;
        }

        if (diff == 1){
            return 1;
        }
        else{
            return 0;
        }
    }
    else if (strlen(word1) == strlen(word2) + 1 || strlen(word1) + 1 == strlen(word2)){
        
        int diff = 0;  
        char *longWord, *shortWord;

        if (strlen(word1) > strlen(word2)){
            longWord = word1;
            shortWord = word2;
        }
        else{
            longWord = word2;
            shortWord = word1;
        }

        int i = 0;
        while (i < strlen(longWord) && i + diff != strlen(longWord)){
            if (*(longWord + i + diff) != *(shortWord + i)){
                diff++;
            }
            else{
                i++;
            }
        }

        if (diff == 1 || diff == 0){
            return 1;
        }
        else{
            return 0;
        }
    }
    else{
        return 0;
    }
}

/*
    Written by Xiao Li, z5139219
    For 17s2, COMP9024 Assignment 2 : Word chains
*/



