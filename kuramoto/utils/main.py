import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path


def load_simulation_data(parquet_path: str) -> pd.DataFrame:
    df = pd.read_parquet(parquet_path)
    return df


def create_circle_animation(
    df: pd.DataFrame,
    output_path: str = "kuramoto_animation.gif",
    fps: int = 30,
    skip_frames: int = 5,
    figsize: tuple = (10, 10),
):
    """
    Create an animated GIF showing oscillators on a unit circle.
    
    Args:
        df: DataFrame with columns [time, oscillator, phase, frequency]
        output_path: Path to save the GIF
        fps: Frames per second in the output GIF
        skip_frames: Only plot every Nth time step (for faster rendering)
    """
    # Get unique time steps
    time_steps = sorted(df['time'].unique())[::skip_frames]
    n_oscillators = df['oscillator'].nunique()
    
    print(f"Creating animation with {len(time_steps)} frames...")
    print(f"Number of oscillators: {n_oscillators}")
    
    # Set up the figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Left plot: Unit circle with oscillators
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('Oscillator Phases', fontsize=14)
    ax1.set_xlabel('cos(θ)')
    ax1.set_ylabel('sin(θ)')
    
    # Draw unit circle
    circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2, alpha=0.3)
    ax1.add_patch(circle)
    
    # Right plot: Phase vs oscillator ID
    ax2.set_xlim(0, n_oscillators)
    ax2.set_ylim(0, 2 * np.pi)
    ax2.set_xlabel('Oscillator ID')
    ax2.set_ylabel('')
    ax2.set_title('Phase Distribution', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_yticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax2.set_yticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    
    # Initialize plot elements
    scatter = ax1.scatter([], [], s=100, c=[], vmin=0, vmax=2*np.pi, alpha=0.7, edgecolors='black')
    lines = [ax1.plot([], [], 'k-', alpha=0.3, linewidth=1)[0] for _ in range(n_oscillators)]
    phase_scatter = ax2.scatter([], [], s=50, c=[], vmin=0, vmax=2*np.pi, alpha=0.7)
    time_text = fig.text(0.5, 0.95, '', ha='center', fontsize=12)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1, fraction=0.046, pad=0.04)
    cbar.set_label('Phase (radians)', rotation=270, labelpad=15)
    cbar.set_ticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    cbar.set_ticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    
    def init():
        """Initialize animation."""
        scatter.set_offsets(np.empty((0, 2)))
        scatter.set_array(np.array([]))
        phase_scatter.set_offsets(np.empty((0, 2)))
        phase_scatter.set_array(np.array([]))
        for line in lines:
            line.set_data([], [])
        time_text.set_text('')
        return [scatter, phase_scatter, time_text] + lines
    
    def update(frame_idx):
        """Update animation frame."""
        time_step = time_steps[frame_idx]
        
        # Get data for this time step
        frame_data = df[df['time'] == time_step].sort_values('oscillator')
        phases = frame_data['phase'].values
        oscillator_ids = frame_data['oscillator'].values
        
        # Convert phases to (x, y) coordinates on unit circle
        x = np.cos(phases)
        y = np.sin(phases)
        
        # Update scatter plot
        scatter.set_offsets(np.c_[x, y])
        scatter.set_array(phases)
        
        # Update lines from origin to each oscillator
        for i, (xi, yi) in enumerate(zip(x, y)):
            lines[i].set_data([0, xi], [0, yi])
        
        # Update phase distribution plot
        phase_scatter.set_offsets(np.c_[oscillator_ids, phases])
        phase_scatter.set_array(phases)
        
        # Update time text
        time_text.set_text(f'Time Step: {time_step} / {time_steps[-1]}')
        
        return [scatter, phase_scatter, time_text] + lines
    
    # Create animation
    anim = FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(time_steps),
        interval=1000/fps,
        blit=True,
        repeat=True
    )
    
    # Save as GIF
    print(f"Saving animation to {output_path}...")
    writer = PillowWriter(fps=fps)
    anim.save(output_path, writer=writer)
    print(f"Animation saved successfully!")
    
    plt.close()


def plot_order_parameter(df: pd.DataFrame, output_path: str = "order_parameter.png"):
    """
    Plot the order parameter over time.
    The order parameter measures synchronization (0 = no sync, 1 = perfect sync).
    
    Args:
        df: DataFrame with columns [time, oscillator, phase, frequency]
        output_path: Path to save the plot
    """
    time_steps = sorted(df['time'].unique())
    order_params = []
    
    for t in time_steps:
        phases = df[df['time'] == t]['phase'].values
        # Order parameter: |⟨e^(iθ)⟩|
        r = np.abs(np.mean(np.exp(1j * phases)))
        order_params.append(r)
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, order_params, linewidth=2)
    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('Order Parameter (r)', fontsize=12)
    plt.title('Kuramoto Order Parameter')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Order parameter plot saved to {output_path}")


def main():
    parquet_path = "../kuramoto.pq"
    gif_output = "kuramoto_animation.gif"
    order_param_output = "order_parameter.png"
    
    # Load data
    print("Loading simulation data...")
    df = load_simulation_data(parquet_path)
    print(f"Loaded {len(df)} rows of data")
    print(f"Time steps: {df['time'].min()} to {df['time'].max()}")
    print(f"Number of oscillators: {df['oscillator'].nunique()}")
    
    # Create animations and plots
    create_circle_animation(
        df,
        output_path=gif_output,
        fps=30,
        skip_frames=5,  # Only plot every 5th frame for faster rendering
        figsize=(14, 7)
    )
    
    plot_order_parameter(df, output_path=order_param_output)
    
    print("\nVisualization complete!")
    print(f"  - Animation: {gif_output}")
    print(f"  - Order parameter plot: {order_param_output}")


if __name__ == "__main__":
    main()

