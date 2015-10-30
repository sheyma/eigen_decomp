#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <limits.h>

/* local run command: */
/* $ gcc C_tutorial.c -llapack -o C_tutorial */
/* calling Fortran based function with "_" character, e.g. dsyev_*/

int integer_add(int x, int y)
{
  int result;
  result = x + y;
  return result;
}

struct database
{
  int id_number;
  int age;
  float salary;
};

/* LAPACK library, dsyev function */
/* Intel® Math Kernel Library LAPACK Examples */
/* https://software.intel.com/sites/products/documentation/doclib/mkl_sa/11/mkl_lapack_examples/*/

/* DSYEV prototype */
extern void dsyev_( char* jobz, char* uplo, int* n, double* a, int* lda,
                double* w, double* work, int* lwork, int* info );
/* Auxiliary routines prototypes */
extern void print_matrix( char* desc, int m, int n, double* a, int lda );
/* Parameters */
#define N 5
#define LDA N

int main()
{
  printf("Hello World! \n");
  int sum;
  sum = integer_add( 5, 12);
  printf("The addition of 5 and 12 is %d.\n", sum);
 
  char c1;
  c1 = 'A';
  printf("Convert the value of c1 to character: %c\n", c1);
  
  int int_num1;
  float flt_num1;
  
  int_num1 = 32/11;
  flt_num1 = 32.0/11;
  printf("The integer division of 32/11 is: %d\n", int_num1);
  printf("The floating-point division of 32.0/11 is: %f\n", flt_num1);
  
  /* standard input and output I/O */
  int ch;
  ch = 65; /* the numeric value of A*/
  printf("The character that has numeric value of 65 is:\n");
  putc(ch, stdout );
  printf("\n");
  
  /* structURE */
  struct database employee;
  employee.id_number = 178;
  employee.age = 35;
  employee.salary = 12000.00;
  printf("Employee ID-Number: %d\n", employee.id_number);
  printf("Employee Age: %d\n", employee.age);
  printf("Employee ID-Number: %f\n", employee.salary);
  
    /* array */
  double distance[5] = {44.14, 720.52, 96.08, 468.78, 6.28};
  int *ptr_one;
  ptr_one = (int *)malloc(sizeof(int));
  if (ptr_one == 0)
  {
    printf("ERROR: Out of memory\n");
  }
  
  *ptr_one = 25;
  printf("%d\n", *ptr_one);
  free(ptr_one);
  
  /* use function dsyev of LAPACK */ 
  /* Locals */
  int n=N, lda=LDA, info, lwork;
  double wkopt;
  double* work;
  /* Local arrays */
  double w[N];
  double a[LDA*N] = {
              1.96,  -6.49,  -0.47,  7.20,  -0.65,
           -6.49,  3.80,  -6.39,  1.50,  -6.34,
           -0.47, -6.39,  4.17,  -1.51,  2.67,
           -7.20,  1.50, -1.51,  5.70,  1.80,
           -0.65, -6.34,  2.67,  1.80, -7.10
  };
  
  printf("LAPACK - dsyev_ example program results\n");
  /* Query and allocate the optimal workspace */
  lwork = -1;
  dsyev_("Vectors", "Upper", &n, a, &lda, w, &wkopt, &lwork, &info);
  lwork = (int)wkopt;
  work = (double*)malloc( lwork*sizeof(double) );
  /* Solve eigenproblem*/
  dsyev_("Vectors", "Upper", &n, a, &lda, w, work, &lwork, &info);
  /* check for convergence */
  if( info > 0 ) {
    printf( "The algorithm failed to compute eigenvalues.\n" );
    exit( 1 );
  }
  /* print eigenvalues */
  print_matrix("Eigenvalues", 1, n, w, 1);
  /* print eigenvectors */
  print_matrix("Eigenvectors (stored columnwise)", n, n, a, lda);
  exit(0);
}

/* Auxiliary routine: printing a matrix */
void print_matrix( char* desc, int m, int n, double* a, int lda ) {
        int i, j;
        printf( "\n %s\n", desc );
        for( i = 0; i < m; i++ ) {
                for( j = 0; j < n; j++ ) printf( " %6.2f", a[i+j*lda] );
                printf( "\n" );
        }
}