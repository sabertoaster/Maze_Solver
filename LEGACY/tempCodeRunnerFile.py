if finding_index < len(sol.visited):
            position = sol.visited[finding_index]

            # cell_rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)

            # pygame.draw.rect(screen, (0,255,0), cell_rect)

            pygame.draw.circle(screen, (30, 50, 163), [int((position[1] + 0.5) * cell_size), int((position[0] + 0.5) * cell_size)], cell_size // 2 - 1)

            finding_index += 1