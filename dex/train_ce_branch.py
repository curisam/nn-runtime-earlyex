"""Train Cross entropy branch main function"""
import yaml
import argparse
from early_ex.utils import *
from early_ex.model.devour import DevourModel
from early_ex.model.backbone import get_backbone
from early_ex.trainer.dce_branch import DCEBranchTrainer

def main():
    """Train backbone main function"""
    print("Devour & Branch Trainer v0.9")
    cfg = config("./early_ex/configs/base.yml")
    backbone = get_backbone(cfg)

    model = DevourModel(cfg, N=cfg['num_exits'], backbone=backbone)
    trainer = DCEBranchTrainer(model, cfg)
    model = model.to(cfg['device'])
    torch.cuda.synchronize()
    try:
        for epoch in range(60):
            trainer.branch_train(epoch)
            trainer.scheduler.step()
            trainer.branch_visualize(epoch)
    except KeyboardInterrupt:
        print("terminating backbone training")
    trainer.branch_visualize(epoch)
    trainer.branch_test()
        
    model_scripted = torch.jit.script(model) # Export to TorchScript
    model_scripted.save('./model.pt') # Save
    
    model_scripted = torch.jit.script(backbone)
    model_scripted.save('./backbone.pt')

if __name__ == "__main__":
    main()
