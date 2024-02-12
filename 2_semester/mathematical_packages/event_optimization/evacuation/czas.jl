using Plots
using Random

# Program oblicza średni czas wykonania 50 symulacji ewakuacji (tylko 50 z powodu dużej złożoności)
# Poza tym program niczym nie różni się od pojedynczych symulacji w pozostałych plikach
# Testy były wykonywanie przez zamienianie funkcji create_layout oraz add_people na poszczególne typy eventów
# Program nie zwraca gifu

function create_layout(n)  #tworzy szablon pomieszczenia, n - wymiar planszy
    layer = zeros(n, n)
    layer[1,:] .= 1
    layer[n,:] .= 1
    layer[:,1] .= 1
    layer[:,n] .= 1
    layer[n, Int(ceil(n/2))] = 2
    layer[7, 6:11] .= 1
    layer[7:12, 9] .= 1
    layer[12, 9:13] .= 1
    layer[16, 8] = 1
    layer[16, 10] = 1
    return layer
end

function cell_values_layer(map_layout, n) #tworzy warstwę z wartościami pól (odległościami od wyjścia), n - wymiar planszy
    value_map = copy(map_layout)
    value_map[value_map .== 1] .= -1 #zamieniam żeby uniknąć kolizji oznaczeń
    value_map[value_map .== 2] .= 1  #wyjście ma odległość 1
    prev_value = 1

    while 0 in value_map #dopóki są komórki bez obliczonej odległości
        current_value = prev_value + 1 
        for i in 2:n-1, j in 2:n-1
            if prev_value in value_map[i-1:i+1, j-1:j+1] && value_map[i, j] == 0
                value_map[i, j] = current_value
            end
        end
        prev_value += 1
    end
    return value_map
end

function add_people(map_layout, P) # dodaje ludzi na planszę, P - ilość ludzi, map_layout - szablon planszy
    people = 0
    people_place = []
    while people != P
        cell_x = rand(2:n-1)
        cell_y = rand(2:n-1)
        if map_layout[cell_x, cell_y] == 0
            people += 1
            map_layout[cell_x, cell_y] = 3
            push!(people_place, (cell_x, cell_y))
        end
    end
    return (map_layout, people_place)
end

function clear_people(map_layout) #usuwa ludzi w celu przeprowadzenia ponownej symulacji
    map_layout[map_layout .== 3] .= 0
end

function choose(array) #wybiera losowy element z listy
    len = length(array)
    id = rand(1:len)
    return array[id]
end

function move(map_layout, value_map, people_place) #obsługuje ruch ludzi, people_place - lista pozycji wszytskich ludzi
    for p in 1:length(people_place) # p to numer komórki w liście ludzi
        if people_place[p] == false #jeśli dany agent juz wyszedł przejdź do kolejnego
            continue
        end
        x = people_place[p][1] #współrzędna x p-tego agenta
        y = people_place[p][2] #współrzędna y p-tego agenta
        av_cells = [] #komórki, do których można się przenieść
        av_equal_cells = [] #komórki, do których można się przenieść o tej samej odległości
        for i in x-1:x+1, j in y-1:y+1
            if (map_layout[i, j] == 0 || map_layout[i, j] == 2) && value_map[i, j] == value_map[x, y] - 1 #pole jest puste/wyjściem
                push!(av_cells, (i, j))
            elseif (map_layout[i, j] == 0 || map_layout[i, j] == 2) && value_map[i, j] == value_map[x, y] #pole jest puste/wyjściem
                push!(av_equal_cells, (i, j))
            end
        end

        if length(av_cells) != 0 #jeśli są dostępne komórki
            old_coords = people_place[p] #stare współrzędne agenta
            new_coords = choose(av_cells) #nowe współrzędne agenta
            people_place[p] = new_coords #zmiana współrzędnych agenta
            if value_map[people_place[p][1], people_place[p][2]] == 1 #jeśli agent jest w drzwiach
                map_layout[old_coords[1], old_coords[2]] = 0 #wychodzi, więc pole zostaje puste
                people_place[p] = false
            else
                (map_layout[old_coords[1], old_coords[2]], map_layout[new_coords[1], new_coords[2]]) = 
                (map_layout[new_coords[1], new_coords[2]], map_layout[old_coords[1], old_coords[2]]) #zamieniam pola na planszy
            end
        else 
            if length(av_equal_cells) != 0 #jeśli są dostępne komórki równe, ale nie ma lepszych (reszta tak jak powyżej)
                old_coords = people_place[p] 
                new_coords = choose(av_equal_cells) 
                people_place[p] = new_coords 
                if value_map[people_place[p][1], people_place[p][2]] == 1 
                    map_layout[old_coords[1], old_coords[2]] = 0
                    people_place[p] = false
                else
                    (map_layout[old_coords[1], old_coords[2]], map_layout[new_coords[1], new_coords[2]]) = 
                    (map_layout[new_coords[1], new_coords[2]], map_layout[old_coords[1], old_coords[2]]) #zamieniam pola na planszy
                end
            end
        end

    end
end

function evacuation(map_layout, value_map, people_place) #zwraca czas ewakuacji
    t = 0
    while 3 in map_layout
        t += 1
        move(map_layout, value_map, people_place)
    end
    return t
end

function average_time(map_layout, value_map)
    suma = 0
    for i in 1:50
        (map_layout, people_place) = add_people(map_layout, P)
        suma += evacuation(map_layout, value_map, people_place)
        clear_people(map_layout)
        empty!(people_place)
        println(i)
    end
    return suma/50
end

n = 17
P = 40
map_layout = create_layout(n) #kształt planszy
value_map = cell_values_layer(map_layout, n) #plansza z wartościami pól
println(average_time(map_layout, value_map))