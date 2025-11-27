/* c_utility/calculate_change.c */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
    if(argc < 3){ printf("Usage: calculate_change total amount\n"); return 1; }
    double total = atof(argv[1]);
    double paid = atof(argv[2]);
    if(paid < total){
        printf("Insufficient: need %.2f more\n", total - paid);
        return 2;
    }
    printf("Change: %.2f\n", paid - total);
    return 0;
}
