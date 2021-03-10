#include <iostream>
#include <cstdlib>
#include <string>
#include <cmath>

int main(int argc, char* argv[]){
    std::string arg = argv[1];
    float x;

    try {
        std::size_t pos;
        x = std::stoi(arg, &pos);
        if (pos < arg.size()) {
            std::cerr << "Trailing characters after number: " << arg << '\n';
        }
    } catch (std::invalid_argument const &ex) {
        std::cerr << "Invalid number: " << arg << '\n';
    } catch (std::out_of_range const &ex) {
        std::cerr << "Number out of range: " << arg << '\n';
    }

    for(float i=1; i <= x; i++){
        if(x/i == std::floor(x/i)){
            std::cout << i << " is a factor of " << x << "\n";
        }
    }
}