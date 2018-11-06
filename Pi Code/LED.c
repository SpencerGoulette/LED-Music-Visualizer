#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <time.h>
#include <fcntl.h>

int gpio_enable(int gpio);
int gpio_set_output(int gpio);
int gpio_set_output_low(int gpio);
int gpio_set_output_high(int gpio);
int gpio_set_color(int gpio, char color);
int set_color_low(int gpio);
int set_color_high(int gpio);
void ndelay(int time);

#define tHigh 2
#define tLow 1

int main(void)
{
	gpio_enable(17);
	gpio_set_output(17);
	printf("%lf\n",CLOCKS_PER_SEC);
	gpio_set_color(17,'r');
	return 0;
}

int gpio_set_color(int gpio, char color)
{
	if(color == 'r')
	{
		for(int i = 0; i < 24; i++)
		{
			if(i < 8) {
				set_color_high(gpio);
			}
			else
			{
				set_color_low(gpio);
			}
		}	
	}

	return 0;
}

int set_color_high(int gpio)
{
	clock_t start, end;
	start = clock();
	struct timespec tim1, tim2;
	tim1.tv_sec = 0;
	tim1.tv_nsec = tLow;
	gpio_set_output_high(gpio);
	if(nanosleep(&tim1, &tim2) < 0)
	{
		printf("Nano sleep system call failed \n");
		return -1;
	}
	gpio_set_output_low(gpio);
	tim1.tv_nsec = tHigh;
	if(nanosleep(&tim1, &tim2) < 0)
	{
		printf("Nano sleep system call failed \n");
		return -1;
	}
	end = clock();
	printf("%lf\n", ((double)(end - start)) / CLOCKS_PER_SEC);
	return 0;
}

int set_color_low(int gpio)
{
	struct timespec tim1, tim2;
	tim1.tv_sec = 0;
	tim1.tv_nsec = tHigh;
	gpio_set_output_high(gpio);
	if(nanosleep(&tim1, &tim2) < 0)
	{
		printf("Nano sleep system call failed \n");
		return -1;
	}
	gpio_set_output_low(gpio);
	tim1.tv_nsec = tLow;
	if(nanosleep(&tim1, &tim2) < 0)
	{
		printf("Nano sleep system call failed \n");
		return -1;
	}

	return 0;
}

void ndelay(int time)
{
	for(int i = 0; i < time; i++);
	return;
}

int gpio_set_output_high(int gpio)
{
	int fd;
	char string[BUFSIZ];

	sprintf(string,"/sys/class/gpio/gpio%d/value",gpio);

	fd = open(string,O_RDWR);
	write(fd,"1",1);
	close(fd);

	return 0;
}

int gpio_set_output_low(int gpio)
{
	int fd;
	char string[BUFSIZ];

	sprintf(string,"/sys/class/gpio/gpio%d/value",gpio);

	fd = open(string,O_RDWR);
	write(fd,"0",1);
	close(fd);

	return 0;
}

int gpio_set_output(int gpio)
{
	FILE *fd;
	char string[BUFSIZ];

	sprintf(string,"/sys/class/gpio/gpio%d/direction",gpio);

	fd = fopen(string,"w");
	if(fd < 0)
	{
		fprintf(stderr,"\tError setting direction of GPIO%d!\n",gpio);
		return -1;
	}	
	fprintf(fd,"out\n");
	fclose(fd);

	return 0;
}

int gpio_enable(int gpio)
{
	FILE *fd;

	fd = fopen("/sys/class/gpio/export","w");
	if(fd < 0)
	{
		fprintf(stderr, "\tError enabling GPIO%d!\n",gpio);
		return -1;
	}
	fprintf(fd, "%d\n", gpio);
	fclose(fd);

	return 0;
}

