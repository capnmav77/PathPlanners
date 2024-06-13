#include <bits/stdc++.h>
#include <cmath>
using namespace std;

class Mapgen {
public:
    vector<vector<vector<int>>> Generate_map(int x, int y, int z, int num_elevators, bool elevator_placement_middle) {
        vector<vector<vector<int>>> map(y, vector<vector<int>>(x, vector<int>(z, 0)));

        // Elevator placement middle
        double x_z_ratio = static_cast<double>(x) / (x + z);
        int num_elevators_x = round(num_elevators * x_z_ratio);
        int num_elevators_z = num_elevators - num_elevators_x;
        int x_elevator_spacing = x / (num_elevators_x + 1);
        int z_elevator_spacing = z / (num_elevators_z + 1);

        if (elevator_placement_middle) {
            // Elevator placement middle
            // placing elevators in the middle of the map
            for (int i = 1; i <= num_elevators_x; i++) {
                for (int j = 1; j <= num_elevators_z; j++) {
                    for (int k = 0; k < y; k++) {
                        map[k][i * x_elevator_spacing][j * z_elevator_spacing] = -1;
                    }
                }
            }
        } else {
            // Elevator placement corner
            int elevators_placed = 0;
            int x_gap = x, z_gap = z;
            bool top = true;
            while (elevators_placed < num_elevators) {
                // First, place the elevators in the 4 corners
                if (elevators_placed < 4) {
                    for (int i = 0; i < 2; i++) {
                        for (int j = 0; j < 2; j++) {
                            for (int k = 0; k < y; k++) {
                                map[k][i * (x - 1)][j * (z - 1)] = -1;
                            }
                            elevators_placed++;
                            if (elevators_placed == num_elevators)
                                break;
                        }
                        if (elevators_placed == num_elevators)
                            break;
                    }
                } else {
                    if(top){
                        if (elevators_placed == num_elevators)
                            break;
                        x_gap = x_gap/2;
                        for(int i=0 ; i<y ; ++i){
                            map[i][x_gap+1][0] = -1;
                        }
                        elevators_placed++;
                        if (elevators_placed == num_elevators)
                            break;
                        for(int i=0 ; i<y ; ++i){
                            map[i][x_gap+1][z-1] = -1;
                        }
                        elevators_placed++;
                        top = false;
                    }
                    else{
                        if(elevators_placed == num_elevators)
                            break;
                        z_gap = z_gap/2;
                        for(int i=0 ; i<y ; i++){
                            map[i][0][z_gap] = -1;
                        }
                        elevators_placed++;
                        if (elevators_placed == num_elevators)
                            break;
                        for(int i=0 ; i<y ; i++){
                            map[i][x-1][z_gap] = -1;
                        }
                        elevators_placed++;
                        top = true;
                    }
                }
            }
        }
        return map;
    }

    void print_map(vector<vector<vector<int>>>& map) {
        for (int i = 0; i < map.size(); i++) {
            for (int j = 0; j < map[0].size(); j++) {
                for (int k = 0; k < map[0][0].size(); k++) {
                    cout << map[i][j][k] << " ";
                }
                cout << endl;
            }
            cout << endl;
            cout << "-----------------" << endl;
        }
    }
};

int main() {
    Mapgen gen;
    vector<vector<vector<int>>> map = gen.Generate_map(10, 5, 10, 4, false);
    gen.print_map(map);
    return 0;
}