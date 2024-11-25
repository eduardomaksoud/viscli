import os
import subprocess
import click

@click.command("run")
@click.option("--scripts-dir", type=click.Path(exists=True), required=True, help="Directory containing Python scripts.")
@click.option("--output-dir", type=click.Path(), required=True, help="Directory to save generated visualization images.")
def run_command(scripts_dir, output_dir):
    """
    Execute Python scripts to generate visualizations and save them as images.
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Iterate through each Python script in the scripts directory
        for script in sorted(os.listdir(scripts_dir)):
            if script.endswith(".py"):
                script_path = os.path.join(scripts_dir, script)
                script_name = os.path.splitext(script)[0]
                image_name = f"{script_name}.png"
                output_image_path = os.path.join(output_dir, image_name)

                # Modify the script to ensure the plot is saved correctly
                modified_script_path = modify_script_to_save_image(script_path, output_image_path)

                click.echo(f"Running script: {script}")
                # Execute the script
                result = subprocess.run(
                    ["python", modified_script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Check for errors in execution
                if result.returncode == 0:
                    click.echo(f"Visualization saved: {output_image_path}")
                else:
                    click.echo(f"Error in script {script}: {result.stderr}")

    except Exception as e:
        click.echo(f"Error executing scripts: {e}")


def modify_script_to_save_image(script_path, output_image_path):
    """
    Ensure the Python script saves the visualization to the specified output path.
    Creates a modified script that explicitly saves the plot to the given path.
    """
    try:
        with open(script_path, "r") as original_script:
            code_lines = original_script.readlines()

        # Look for the savefig line or add one at the end
        modified_code = []
        found_savefig = False
        for line in code_lines:
            if "plt.savefig" in line:
                line = f"plt.savefig('{output_image_path}', bbox_inches='tight')\n"
                found_savefig = True
            modified_code.append(line)

        # Add savefig if not already present
        if not found_savefig:
            modified_code.append(f"plt.savefig('{output_image_path}', bbox_inches='tight')\n")

        # Write the modified script to a temporary file
        modified_script_path = script_path + "_modified"
        with open(modified_script_path, "w") as modified_script:
            modified_script.writelines(modified_code)

        return modified_script_path

    except Exception as e:
        click.echo(f"Error modifying script {script_path}: {e}")
        return script_path
