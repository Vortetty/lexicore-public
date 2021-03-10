#include "rang.hpp"
#include <iostream>
#include <vector>
#include <conio.h>
#include <deque>
#include <random>

#define KEY_ESCAPE 27
#define KEY_UP 72
#define KEY_DOWN 80
#define KEY_LEFT 75
#define KEY_RIGHT 77

using std::string;
using std::vector;
using std::deque;

#if defined(__WIN32__) || defined(_WIN32) || defined(WIN32) || defined(__WINDOWS__) || defined(__TOS_WIN__)
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);

    void gotoxy(short x, short y){
        COORD pos = {x, y};
        SetConsoleCursorPosition(hConsole, pos);
    }
    void clear(void)
    {
        system("cls");
    }

    inline void delay( unsigned long ms )
    {
        Sleep( ms );
        std::cout << "";
    }
#else  /* presume POSIX */
    #include <unistd.h>
    inline void delay( unsigned long ms )
    {
        usleep( ms * 1000 );
    }

    void gotoxy(int x,int y)    
    {
        printf("%c[%d;%df",0x1B,y,x);
    }
    void clrscr(void)
    {
        system("clear");
    }
#endif


char ch;
byte getDirection(){
    if(kbhit()){
        ch = _getch();
    }
    switch(ch){
        case 'A':
        case 'a':
        case KEY_LEFT:
            gotoxy(0, 11);
            std::cout << "Left ";
            return 0;
            break;
        case 'D':
        case 'd':
        case KEY_RIGHT:
            gotoxy(0, 11);
            std::cout << "Right";
            return 1;
            break;
        case 'W':
        case 'w':
        case KEY_UP:
            gotoxy(0, 11);
            std::cout << "Up   ";
            return 2;
            break;
        case 's':
        case 'S':
        case KEY_DOWN:
            gotoxy(0, 11);
            std::cout << "Down ";
            return 3;
            break;
        default:
            gotoxy(0, 11);
            std::cout << (int)ch << "     ";
            break;
            //return 4;
    }
    return 0;
}

bool calcMove(short(* pos)[2], byte dir){
    switch(dir){
        case 0:
            gotoxy(0, 12);
            std::cout << "Left ";
            *pos[0] = *pos[0] - 1;
            break;
        case 1:
            gotoxy(0, 12);
            std::cout << "Right";
            *pos[0] = *pos[0] + 1;
            break;
        case 2:
            gotoxy(0, 12);
            std::cout << "Up   ";
            *pos[1] = *pos[1] - 1;
            break;
        case 3:
            gotoxy(0, 12);
            std::cout << "Down ";
            *pos[1] = *pos[1] + 1;
            break;
    }

    if((0 <= *pos[0] <= 9) && (0 <= *pos[1] <= 9)){
        return true;
    }
    return false;
}

int main(){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 9);

    short snekHeadPos[2] = {0, 0};

    deque<short*> snek;
    snek.push_back(snekHeadPos);

    short foodPos[2] = {
        (short)dis(gen),
        (short)dis(gen)
    };

    // 0: left
    // 1: right
    // 2: up
    // 3: down
    byte snekDir = 1;

    while(true){
        snekDir = getDirection();

        short tempSnekPos[2];
        bool notHitSide = calcMove(&tempSnekPos, snekDir);

        if (std::find(snek.begin(), snek.end(), tempSnekPos) != snek.end()){
            //return 0;
            gotoxy(0,10);
            std::cout << "tried to exit due to wrong head spot";
        }
        else if (!notHitSide){
            gotoxy(0,10);
            std::cout << "tried to exit due to out of bounds";
        }
        else if (snekDir == 4){
            return 0;
        }

        if(foodPos == snekHeadPos){
            foodPos[0] = (short)dis(gen);
            foodPos[1] = (short)dis(gen);
        }
        else{
            //snek.pop_front();
        }

        snek.push_back(tempSnekPos);
        snekHeadPos[0] = tempSnekPos[0];
        snekHeadPos[1] = tempSnekPos[1];

        for(int y = 0; y < 9; y++){
            for(int x = 0; x < 9; x++){
                gotoxy(x * 3, y);
                std::cout << rang::fgB::gray << "__ ";
            }
        }
        for (int i = 0; i < snek.size(); i++){
            gotoxy(0,13);
            std::cout << snek[i][0] << ", " << snek[i][1];
            
            gotoxy(snek[i][0]*3, snek[i][1]);
            std::cout << rang::fgB::green << "()";
        }
        gotoxy(foodPos[0]*3, foodPos[1]);
        std::cout << rang::fgB::red << "[]";

        delay(1000);
    }
}