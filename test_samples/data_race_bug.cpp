#include <iostream>
#include <thread>
#include <vector>

// Shared variable
int counter = 0;

// Function to increment the counter
void incrementCounter( ) {
    for ( int i = 0; i < 1000; ++i ) {
        ++counter; // Data race occurs here
        }
    }

int main( ) {
    // Create multiple threads
    std::vector<std::thread> threads;
    for ( int i = 0; i < 10; ++i ) {
        threads.emplace_back( incrementCounter );
        }

        // Join all threads
    for ( auto & t : threads ) {
        t.join( );
        }

        // Print the final value of the counter
    std::cout << "Final counter value: " << counter << std::endl;

    return 0;
    }