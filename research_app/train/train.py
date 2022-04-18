import os

import flash
from flash.core.data.utils import download_data
from flash.image import ImageClassificationData, ImageClassifier

train_script_path = __file__

if not os.environ.get("WANDB_API_KEY"):
    os.environ["WANDB_API_KEY"] = "91a1bdb7f2221dea67aba711651976435a50b4a5"

if __name__ == "__main__":
    # 1. Create the DataModule
    download_data(
        "https://pl-flash-data.s3.amazonaws.com/hymenoptera_data.zip", "./data"
    )  # E501

    datamodule = ImageClassificationData.from_folders(
        train_folder="data/hymenoptera_data/train/",
        val_folder="data/hymenoptera_data/val/",
        batch_size=4,
        transform_kwargs={
            "image_size": (196, 196),
            "mean": (0.485, 0.456, 0.406),
            "std": (0.229, 0.224, 0.225),
        },
    )

    # 2. Build the task
    model = ImageClassifier(backbone="resnet18", labels=datamodule.labels)

    # 3. Create the trainer and finetune the model
    trainer = flash.Trainer(max_epochs=1)
    trainer.finetune(model, datamodule=datamodule, strategy="freeze")
    trainer.save_checkpoint("image_classification_model.pt")
    print("training finished!")
