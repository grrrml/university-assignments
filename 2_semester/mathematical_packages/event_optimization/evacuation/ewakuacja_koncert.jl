using Plots
using Random

#=
Wersja 2: Ludzie nie ustawiają się w "kolejce po skosie",
szukają innej optymalnej drogi idąc na pola o równej wartości

Odległość mierzona w metryce Czebyszewa

Oznaczenia:
W szablonie: 0 = puste pole ; 1 = ściana ; 2 = wyjście ; 3 = osoba
W warstwie liczacej odległość(cell_values_layer): -1 = ściana ; >=1 = odległość od wyjścia
=#

function create_layout(bramki)  #tworzy szablon pomieszczenia, n - wymiar kwadratowej planszy
    n = 100
    layer = zeros(n, n)
    layer[1,:] .= 1
    layer[n,:] .= 1
    layer[:,1] .= 1
    layer[:,n] .= 1
    layer[n,Int(ceil(1n/5)):Int(ceil(4n/5))] .= 2
    layer[Int(ceil(4n/5)),:] .= 1
    layer[Int(ceil(4n/5)),Int(ceil(n/2))-bramki+1:2:Int(ceil(n/2))+bramki-1] .= 0
    layer[2:10,(-25+Int(ceil(n/2))):(25+Int(ceil(n/2)))] .= 1
    layer[2:20,(-7+Int(ceil(n/2))):(7+Int(ceil(n/2)))] .= 1

    return layer
end

function cell_values_layer(map_layout) #tworzy warstwę z wartościami pól (odległościami od wyjścia), n - wymiar planszy
    n = 100
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
    n = 100
    people = 0
    people_place = []
    while people != P
        cell_x = rand(2:Int(4n/5-10))
        cell_y = rand(2:n-1)
        if map_layout[cell_x, cell_y] == 0
            people += 1
            map_layout[cell_x, cell_y] = 3
            push!(people_place, (cell_x, cell_y))
        end
    end
    return (map_layout, people_place)
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

function evacuation(map_layout, value_map, people_place) #gif ewakuacji, wypisuje czas ewakuacji
    an = Animation()
    t = 0
    while 3 in map_layout
        t += 1
        map = heatmap(map_layout,
        aspect_ratio = 1,
        seriescolor = palette([:white, :black, :lime, :blue]),
        colorbar = false,
        xlims = (0, size(map_layout, 1)),
        ylims = (0, size(map_layout, 2))
        )
        frame(an, map)
        move(map_layout, value_map, people_place)
    end
    println(t)
    return gif(an, fps=5)
end

function draw_layout(matrix) #(rysunek) szablon planszy z ludźmi
    heatmap(matrix,
        aspect_ratio = 1,
        seriescolor = palette([:white, :black, :lime, :blue]),
        colorbar = false,
        xlims = (0, size(matrix, 1)),
        ylims = (0, size(matrix, 2))
        )  
end

function draw_value_map(matrix) #(rysunek) pokazuje odległość każdego pola od wyjścia
    heatmap(matrix,
        aspect_ratio = 1,
        seriescolor = cgrad([:yellow,:darkred]),
        xlims = (0, size(matrix, 1)),
        ylims = (0, size(matrix, 2)),
        title = "Odległość od wyjścia"    
        ) 
end

P = 3000
bramki = 19
map_layout = create_layout(bramki) #kształt planszy
value_map = cell_values_layer(map_layout) #plansza z wartościami pól
(map_layout, people_place) = add_people(map_layout, P) #plansza z ludźmi, położenie ludzi w wektorze
evacuation(map_layout, value_map, people_place)