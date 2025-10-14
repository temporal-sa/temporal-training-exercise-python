from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from transfer_request import TransferRequest

with workflow.unsafe.imports_passed_through():
    from banking_activities import withdraw, deposit, refund


@workflow.defn
class MoneyTransferWorkflow:
    def __init__(self) -> None:
        self.approved = False
        self.approval_received = False
        self.transfer_state = "PENDING"
        self.current_step = "INITIALIZED"

    @workflow.run
    async def transfer(self, request: TransferRequest) -> str:
        workflow.logger.info(f"Starting transfer: {request}")
        self.transfer_state = "IN_PROGRESS"
        self.current_step = "WITHDRAWING"
        
        # Step 1: Withdraw from source account
        # TODO: Add activity summary for withdraw operation
        # Use workflow.execute_activity with summary parameter
        await workflow.execute_activity(
            withdraw,
            args=[request.from_account, request.amount],
            start_to_close_timeout=timedelta(seconds=5),
            # TODO: Add summary="Withdrawing funds from account {account_id}"
        )
        
        workflow.logger.info("Withdrawal completed")
        self.current_step = "WAITING_FOR_APPROVAL"
        
        # Step 2: Wait for approval
        workflow.logger.info("Waiting for approval...")
        await workflow.wait_condition(lambda: self.approval_received)
        
        if self.approved:
            # Step 3a: If approved, execute deposit activity
            self.current_step = "DEPOSITING"
            # TODO: Add activity summary for deposit operation
            await workflow.execute_activity(
                deposit,
                args=[request.to_account, request.amount],
                start_to_close_timeout=timedelta(seconds=5),
                # TODO: Add summary="Depositing funds to account {account_id}"
            )
            
            workflow.logger.info("Transfer approved and completed")
            self.transfer_state = "COMPLETED"
            self.current_step = "COMPLETED"
            return "Transfer completed successfully"
        else:
            # Step 3b: If not approved, execute refund activity
            self.current_step = "REFUNDING"
            # TODO: Add activity summary for refund operation
            await workflow.execute_activity(
                refund,
                args=[request.from_account, request.amount],
                start_to_close_timeout=timedelta(seconds=5),
                # TODO: Add summary="Refunding funds to account {account_id}"
            )
            
            workflow.logger.info("Transfer rejected and refunded")
            self.transfer_state = "REJECTED"
            self.current_step = "REFUNDED"
            return "Transfer rejected and refunded"

    @workflow.signal
    async def approve(self, approved: bool) -> None:
        workflow.logger.info(f"Approval received: {approved}")
        self.approved = approved
        self.approval_received = True

    @workflow.query
    def get_transfer_state(self) -> str:
        return self.transfer_state

    @workflow.query
    def get_current_step(self) -> str:
        return self.current_step

    @workflow.query
    def is_approved(self) -> bool:
        return self.approved if self.approval_received else None